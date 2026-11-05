# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx>=1.1,<2"]
# ///
"""Fill the bundled quotation template from an explicit JSON input file.

Usage: uv run fill_quotation.py INPUT.json OUTPUT.docx [--template TEMPLATE.docx]

The script lays out what it is given; it does not decide how an offer charges. Items,
amounts and the totals box come from the input as displayed values. Numeric amounts are
formatted, and an item whose unit price, quantity and total are all numeric is checked.
Nothing is defaulted except the company's standard remarks, which the input can replace.
"""

import argparse
import copy
import json
import math
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "quotation-template.docx"
CENT = Decimal("0.01")
ISSUER_SIGNATORIES = 2  # company standard: two signature fields on our side
REQUIRED = {
    "issuer": ["tin", "address", "website"],  # the name is in the template logo
    "customer": ["name"],
    "quotation": ["number", "date", "project"],
}
OPTIONAL = {"customer": ["address", "contact_name", "contact"]}
CURRENCY_NAMES = {"PHP": "Philippine Pesos", "USD": "US Dollars", "TWD": "New Taiwan Dollars"}
VAT_LABELS = {"exclusive": "VAT Excl.", "inclusive": "VAT Incl."}
DEFAULT_PAYMENT_TERMS = "As stipulated in the Agreement."


class InputError(ValueError):
    pass


def present(data, key):
    value = data.get(key) if isinstance(data, dict) else None
    return value if isinstance(value, str) and value.strip() else None


def number(value):
    """Decimal for an int or numeric string, else None. Floats are rejected by the caller."""
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    try:
        result = Decimal(str(value).replace(",", "").strip())
    except InvalidOperation:
        return None
    return result if result.is_finite() else None


def money(value):
    """Group thousands; show at least two decimals and never round a given precision away."""
    if value.as_tuple().exponent > -2:
        value = value.quantize(CENT)
    return f"{value:,f}"


def display(value, where, problems, amount=True):
    """Text to show for a value: numbers formatted, other text verbatim."""
    if value is None:
        return ""
    if isinstance(value, float):
        problems.append(f"{where} must be a string or integer (not a float)")
        return ""
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        problems.append(f"{where} must be a string or integer")
        return ""
    n = number(value)
    if n is None:
        return str(value).strip()
    return money(n) if amount else f"{n:,f}"


def standard_terms(q):
    """Company standard remarks; extra remarks go before the payment terms."""
    taxes = "exclusive of taxes" if q["vat_basis"] == "exclusive" else "inclusive of taxes"
    terms = [
        f"The amounts stated in this quotation are in {q['currency_name']} ({q['currency']})"
        f" and are {taxes}. This quotation shall remain valid before"
        f" {q['quotation']['valid_until']}.",
        "This quotation shall become effective only upon signature by the authorized signatories.",
        "Upon acceptance and return of the signed quotation by the Customer, the quotation"
        " shall be deemed a reservation. The Customer shall ensure that the signatory is duly"
        " authorized to sign on behalf of the Customer.",
    ]
    if q["master_agreement"]:
        terms.append(
            "Any terms and conditions not specified in this quotation shall be governed by the"
            " master agreement (the “Agreement”) to be entered into subsequently by the"
            " parties. In the event of any inconsistency between the terms and conditions of"
            " this quotation and those of the Agreement, the terms and conditions of the"
            " Agreement shall prevail."
        )
    return [*terms, *q["extra_remarks"], f"Payment Terms: {q['payment_terms']}"]


def text_list(data, key, problems):
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        problems.append(f"{key} must be a list of nonempty strings")
        return []
    return value


def validate(data):
    """Return a normalized quotation or raise InputError listing every problem."""
    problems = []
    if not isinstance(data, dict):
        raise InputError("input must be a JSON object")
    for section, keys in REQUIRED.items():
        for key in keys:
            if present(data.get(section), key) is None:
                problems.append(f"missing {section}.{key}")
    for section, keys in OPTIONAL.items():
        for key in keys:
            value = (data.get(section) or {}).get(key, "")
            if not isinstance(value, str):
                problems.append(f"{section}.{key} must be a string")
    currency = present(data, "currency")
    if currency is None:
        problems.append("missing currency")
    vat_basis = data.get("vat_basis")
    if vat_basis is not None and vat_basis not in VAT_LABELS:
        problems.append("vat_basis must be 'exclusive' or 'inclusive' when given")

    items = []
    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        problems.append("items must be a nonempty list")
        raw_items = []
    for n, raw in enumerate(raw_items, 1):
        where = f"items[{n}]"
        if not isinstance(raw, dict):
            problems.append(f"{where} must be an object")
            continue
        item = {"no": present(raw, "no") or str(n), "title": present(raw, "title")}
        if item["title"] is None:
            problems.append(f"missing {where}.title")
        for key in ("detail", "unit"):
            item[key] = raw.get(key, "")
            if not isinstance(item[key], str):
                problems.append(f"{where}.{key} must be a string")
                item[key] = ""
        item["unit_price"] = display(raw.get("unit_price"), f"{where}.unit_price", problems)
        item["quantity"] = display(raw.get("quantity"), f"{where}.quantity", problems, False)
        item["total"] = display(raw.get("total"), f"{where}.total", problems)
        price, qty, total = (number(raw.get(k)) for k in ("unit_price", "quantity", "total"))
        item["checked"] = None not in (price, qty, total)
        if item["checked"] and (price * qty).quantize(CENT, ROUND_HALF_UP) != total.quantize(
            CENT, ROUND_HALF_UP
        ):
            problems.append(
                f"{where}: unit_price {price} x quantity {qty} = {price * qty}, not total {total}"
            )
        items.append(item)

    summary = data.get("summary", [])
    if not isinstance(summary, list):
        problems.append("summary must be a list")
        summary = []
    lines = []
    for n, line in enumerate(summary, 1):
        keys = ("label", "amount", "suffix")
        if not isinstance(line, dict) or not any(present(line, k) for k in keys):
            problems.append(f"summary[{n}] needs at least one of label, amount, suffix")
            continue
        lines.append(tuple(line.get(k, "") if isinstance(line.get(k), str) else "" for k in keys))

    q = {
        **data,
        "currency": currency,
        "vat_basis": vat_basis,
        "items": items,
        "summary": lines,
        "quotation": data.get("quotation") or {},
    }
    if "remarks" in data:
        q["remarks"] = text_list(data, "remarks", problems)
        if "extra_remarks" in data:
            problems.append("extra_remarks only apply to the standard remarks; put them in remarks")
    else:
        # Standard remarks: their variable parts are required.
        q["extra_remarks"] = text_list(data, "extra_remarks", problems)
        q["currency_name"] = present(data, "currency_name") or CURRENCY_NAMES.get(currency or "")
        if currency and q["currency_name"] is None:
            problems.append(f"missing currency_name for {currency} (e.g. 'Philippine Pesos')")
        if present(q["quotation"], "valid_until") is None:
            problems.append("missing quotation.valid_until (used by the standard remarks)")
        if vat_basis is None:
            problems.append("missing vat_basis (used by the standard remarks)")
        q["master_agreement"] = data.get("master_agreement", True)
        if not isinstance(q["master_agreement"], bool):
            problems.append("master_agreement must be true or false")
        q["payment_terms"] = present(data, "payment_terms")
        if q["payment_terms"] is None:
            if q["master_agreement"] is True:
                q["payment_terms"] = DEFAULT_PAYMENT_TERMS
            else:
                problems.append("missing payment_terms (no master agreement to refer to)")
        if not problems:
            q["remarks"] = standard_terms(q)

    sign = data.get("signatories") if isinstance(data.get("signatories"), dict) else {}
    signatories = {}
    for side in ("issuer", "customer"):
        people = sign.get(side)
        if not isinstance(people, list) or not people:
            problems.append(f"signatories.{side} must be a nonempty list")
            people = []
        elif side == "issuer" and len(people) != ISSUER_SIGNATORIES:
            problems.append(
                f"signatories.issuer needs exactly {ISSUER_SIGNATORIES} signatories, got {len(people)}"
            )
        for n, person in enumerate(people, 1):
            for key in ("role", "name"):
                if present(person, key) is None:
                    problems.append(f"missing signatories.{side}[{n}].{key}")
        signatories[side] = people
    q["signatories"] = signatories
    if problems:
        raise InputError("\n".join(problems))
    return q


# The item table sits inside a fixed-size rounded frame drawn behind the text, sized by
# hand in the source quotation. Re-estimate its height (points) from the content.
HEADER, ROW, LINE, PAD = 24, 3.5, 11, 8
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"
V = "{urn:schemas-microsoft-com:vml}"


def frame_points(items, lines):
    def wrap(text, width):
        return math.ceil(len(text) / width) if text else 0

    def row_lines(i):
        quantity = f"{i['quantity']} {i['unit']}".strip()
        # Word-wrapped narrow columns can be taller than the description.
        return max(
            1,
            wrap(i["title"], 55) + wrap(i["detail"], 70),
            sum(wrap(word, 6) for word in quantity.split()),
            wrap(i["unit_price"], 12),
            wrap(i["total"], 12),
        )

    rows = sum(ROW + LINE * row_lines(i) for i in items)
    return HEADER + rows + LINE * sum(max(1, wrap("".join(line), 140)) for line in lines) + PAD


def resize_item_frame(d, items, lines):
    anchors = list(d.element.body.iter(f"{WP}anchor"))
    if not anchors:
        return
    frame = max(anchors, key=lambda a: int(a.find(f"{WP}extent").get("cy")))
    height = round(frame_points(items, lines) * 12700)  # EMU per point
    frame.find(f"{WP}extent").set("cy", str(height))
    for ext in frame.iter(f"{A}ext"):
        if ext.get("cy"):
            ext.set("cy", str(height))
    choice = frame.getparent().getparent()
    fallback = choice.getparent().find(f"{MC}Fallback") if choice.tag == f"{MC}Choice" else None
    for shape in fallback.iter(f"{V}roundrect") if fallback is not None else ():
        style = re.sub(r"height:[0-9.]+pt", f"height:{height / 12700:.2f}pt", shape.get("style"))
        shape.set("style", style)


def fill(q, template, output):
    import docx

    d = docx.Document(template)
    customer = q["customer"]
    basis = VAT_LABELS.get(q["vat_basis"])
    values = {
        "issuer_tin": q["issuer"]["tin"],
        "issuer_address": q["issuer"]["address"],
        "issuer_website": q["issuer"]["website"],
        "quotation_number": q["quotation"]["number"],
        "quotation_date": q["quotation"]["date"],
        "project": q["quotation"]["project"],
        "customer_name": customer["name"],
        "customer_address": customer.get("address", ""),
        "customer_contact_name": customer.get("contact_name", ""),
        "customer_contact": customer.get("contact", ""),
        "currency": q["currency"],
    }
    column_note = f"({q['currency']}, {basis})" if basis else f"({q['currency']})"

    def substitute(paragraph, mapping):
        # Assign only runs holding a placeholder: setting run.text drops drawings.
        for run in paragraph.runs:
            text = run.text.replace("({{currency}}, {{vat_label}})", column_note)
            for key, value in mapping.items():
                text = text.replace("{{%s}}" % key, str(value))
            if text != run.text:
                run.text = text

    def paragraphs(container):
        yield from container.paragraphs
        for table in container.tables:
            for row in table.rows:
                for cell in row.cells:
                    yield from cell.paragraphs

    _, _, items, signs = d.tables
    proto = items.rows[1]._tr
    for _ in q["items"]:
        proto.addprevious(copy.deepcopy(proto))
    proto.getparent().remove(proto)
    for row, item in zip(items.rows[1:-1], q["items"]):
        mapping = {
            "item_no": item["no"],
            "item_title": item["title"],
            "item_detail": item["detail"],
            "unit_price": item["unit_price"],
            "quantity": f"{item['quantity']} {item['unit']}".strip(),
            "line_total": item["total"],
        }
        for cell in row.cells:
            for p in cell.paragraphs:
                substitute(p, mapping)
            if not item["detail"]:
                for p in cell.paragraphs[1:]:
                    if not p.text:
                        p._p.getparent().remove(p._p)

    total = items.rows[-1].cells[0].paragraphs[0]
    label_run, amount_run = total.runs[0]._r, total.runs[1]._r
    run_type = type(total.runs[0])
    for n, (label, amount, suffix) in enumerate(q["summary"]):
        parts = [(label_run, label), (amount_run, amount), (label_run, suffix)]
        first = True
        for source, text in parts:
            if not text:
                continue
            run = copy.deepcopy(source)
            label_run.addprevious(run)
            run_type(run, total).text = ("\n" if n and first else "") + text
            first = False
    label_run.getparent().remove(label_run)
    amount_run.getparent().remove(amount_run)
    resize_item_frame(d, q["items"], q["summary"])

    remark = next(p for p in d.paragraphs if "{{remark}}" in p.text)
    for text in q["remarks"]:
        new = copy.deepcopy(remark._p)
        remark._p.addprevious(new)
        for t in new.iter(f"{W}t"):
            t.text = t.text.replace("{{remark}}", text)
    remark._p.getparent().remove(remark._p)
    if not q["remarks"]:
        heading = next(p for p in d.paragraphs if p.text.strip() == "Remarks:")
        heading._p.getparent().remove(heading._p)

    issuer, customer_signs = q["signatories"]["issuer"], q["signatories"]["customer"]
    count = max(len(issuer), len(customer_signs))
    protos = [r._tr for r in signs.rows]
    for _ in range(count):
        line, name = (copy.deepcopy(p) for p in protos)
        protos[0].addprevious(line)
        protos[0].addprevious(name)
    for p in protos:
        p.getparent().remove(p)
    rows = list(signs.rows)
    for n in range(count):
        line, name = rows[2 * n], rows[2 * n + 1]
        for col, people in ((0, issuer), (1, customer_signs)):
            side = "issuer" if col == 0 else "customer"
            if n < len(people):
                substitute(
                    name.cells[col].paragraphs[0],
                    {
                        f"{side}_signatory_role": people[n]["role"],
                        f"{side}_signatory_name": people[n]["name"],
                    },
                )
            else:
                for cell in (line.cells[col], name.cells[col]):
                    for p in cell.paragraphs:
                        for r in p.runs:
                            if r.text:
                                r.text = ""

    for p in paragraphs(d):
        substitute(p, values)
    left = [p.text for p in paragraphs(d) if "{{" in p.text]
    if left:
        raise InputError(f"unfilled template placeholders: {left}")
    d.save(output)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--template", type=Path, default=TEMPLATE)
    args = parser.parse_args(argv)
    try:
        q = validate(json.loads(args.input.read_text(encoding="utf-8")))
        if args.output.exists():
            raise InputError(f"refusing to overwrite existing {args.output}")
        fill(q, args.template, args.output)
    except (InputError, json.JSONDecodeError) as exc:
        print(f"Cannot fill quotation:\n{exc}", file=sys.stderr)
        return 2
    report = {
        "output": str(args.output),
        "items": [
            {
                "no": i["no"],
                "unit_price": i["unit_price"],
                "quantity": f"{i['quantity']} {i['unit']}".strip(),
                "total": i["total"],
                "arithmetic_checked": i["checked"],
            }
            for i in q["items"]
        ],
        "summary": ["".join(line) for line in q["summary"]],
        "remarks": q["remarks"],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
