# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx>=1.1,<2"]
# ///
"""Fill the bundled quotation template from an explicit JSON input file.

Usage: uv run fill_quotation.py INPUT.json OUTPUT.docx [--template TEMPLATE.docx]

Every required value must be supplied; nothing is defaulted or looked up. The
computed amounts are printed as JSON for an independent check.
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
CHARGES = {"one-time", "recurring"}
ISSUER_SIGNATORIES = 2  # company standard: two signature fields on our side
REQUIRED = {
    "issuer": ["name", "tin", "address", "website"],
    "customer": ["name", "address", "contact_name", "contact"],
    "quotation": ["number", "date", "project", "valid_until"],
}


class InputError(ValueError):
    pass


def money(value):
    """Group thousands; show at least two decimals and never round a given precision away."""
    if value.as_tuple().exponent > -2:
        value = value.quantize(CENT)
    return f"{value:,f}"


def decimal(value, where, problems):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        problems.append(f"{where} must be a string or integer amount (not a float)")
        return None
    try:
        result = Decimal(str(value).replace(",", ""))
    except InvalidOperation:
        problems.append(f"{where} is not a number: {value!r}")
        return None
    if not result.is_finite():
        problems.append(f"{where} is not a finite number")
        return None
    return result


def present(data, key):
    value = data.get(key) if isinstance(data, dict) else None
    return value if isinstance(value, str) and value.strip() else None


def validate(data):
    """Return a normalized quotation or raise InputError listing every problem."""
    problems = []
    if not isinstance(data, dict):
        raise InputError("input must be a JSON object")
    for section, keys in REQUIRED.items():
        for key in keys:
            if present(data.get(section), key) is None:
                problems.append(f"missing {section}.{key}")
    currency = present(data, "currency")
    if currency is None:
        problems.append("missing currency")
    vat = data.get("vat") if isinstance(data.get("vat"), dict) else {}
    basis = vat.get("basis")
    if basis not in {"exclusive", "inclusive"}:
        problems.append("vat.basis must be 'exclusive' or 'inclusive'")
    rate = decimal(vat["rate"], "vat.rate", problems) if "rate" in vat else None
    if "rate" not in vat:
        problems.append('missing vat.rate (use "0" only when the user confirms zero VAT)')
    elif rate is not None and not Decimal(0) <= rate < 1:
        problems.append('vat.rate must be a fraction such as "0.12"')
    if present(data, "payment_terms") is None:
        problems.append("missing payment_terms")
    remarks = data.get("remarks", [])
    if not isinstance(remarks, list) or not all(isinstance(r, str) and r.strip() for r in remarks):
        problems.append("remarks must be a list of nonempty strings")
        remarks = []

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
        item = {"no": n, "title": present(raw, "title"), "detail": raw.get("detail", "")}
        if item["title"] is None:
            problems.append(f"missing {where}.title")
        if not isinstance(item["detail"], str):
            problems.append(f"{where}.detail must be a string")
        charge = raw.get("charge")
        if charge not in CHARGES:
            problems.append(f"{where}.charge must be 'one-time' or 'recurring'")
        item["charge"] = charge
        item["period"] = present(raw, "period")
        if charge == "recurring" and item["period"] is None:
            problems.append(f"missing {where}.period for a recurring charge (e.g. 'year')")
        qty = decimal(raw["quantity"], f"{where}.quantity", problems) if "quantity" in raw else None
        if "quantity" not in raw:
            problems.append(f"missing {where}.quantity")
        elif qty is not None and qty <= 0:
            problems.append(f"{where}.quantity must be positive")
        item["quantity"], item["unit"] = qty, raw.get("unit", "")
        note = present(raw, "price_note")
        if "unit_price" in raw and note:
            problems.append(f"{where} has both unit_price and price_note")
        elif "unit_price" in raw:
            price = decimal(raw["unit_price"], f"{where}.unit_price", problems)
            if price is not None and price < 0:
                problems.append(f"{where}.unit_price must not be negative")
            item["unit_price"], item["note"] = price, None
        elif note:
            item["unit_price"], item["note"] = None, note
        else:
            problems.append(f"missing {where}.unit_price (or price_note for a variable price)")
        items.append(item)

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
    if problems:
        raise InputError("\n".join(problems))
    return {
        **data,
        "vat": {"basis": basis, "rate": rate},
        "items": items,
        "remarks": remarks,
        "signatories": signatories,
        "currency": currency,
    }


def compute(q):
    """Line totals and per-group totals; variable-priced items are excluded and listed."""
    groups, variable = {}, []
    for item in q["items"]:
        if item["unit_price"] is None:
            item["line_total"] = None
            variable.append(item["no"])
            continue
        item["line_total"] = (item["unit_price"] * item["quantity"]).quantize(CENT, ROUND_HALF_UP)
        key = "one-time" if item["charge"] == "one-time" else f"recurring per {item['period']}"
        groups[key] = groups.get(key, Decimal(0)) + item["line_total"]
    rate, basis = q["vat"]["rate"], q["vat"]["basis"]
    totals = []
    for key in sorted(groups, key=lambda k: (k != "one-time", k)):
        amount = groups[key]
        if basis == "exclusive":
            vat = (amount * rate).quantize(CENT, ROUND_HALF_UP)
            net, gross = amount, amount + vat
        else:
            vat = (amount * rate / (1 + rate)).quantize(CENT, ROUND_HALF_UP)
            net, gross = amount - vat, amount
        totals.append({"group": key, "net": net, "vat": vat, "gross": gross})
    return totals, variable


def total_lines(q, totals, variable):
    cur, pct = q["currency"], f"{(q['vat']['rate'] * 100).normalize():f}%"
    lines = []
    for t in totals:
        label = t["group"].upper()
        if q["vat"]["basis"] == "exclusive":
            lines.append((f"{label} TOTAL (VAT EXCLUSIVE): ", f"{cur} {money(t['net'])}"))
            lines.append(
                (
                    f"VAT ({pct}): {cur} {money(t['vat'])}; total including VAT: ",
                    f"{cur} {money(t['gross'])}",
                )
            )
        else:
            lines.append((f"{label} TOTAL (VAT INCLUSIVE): ", f"{cur} {money(t['gross'])}"))
            lines.append((f"Includes VAT ({pct}) of {cur} {money(t['vat'])}", ""))
    if variable:
        nos = ", ".join(str(n) for n in variable)
        lines.append((f"Totals exclude variable-priced item(s) {nos}.", ""))
    return lines


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
        price = i["note"] or str(i["unit_price"])
        # Word-wrapped narrow columns can be taller than the description.
        return max(
            wrap(i["title"], 55) + wrap(i["detail"], 70),
            math.ceil(len(quantity.split()) / 1.5),
            wrap(price, 10),
        )

    rows = sum(ROW + LINE * row_lines(i) for i in items)
    return HEADER + rows + LINE * sum(max(1, wrap(a + b, 140)) for a, b in lines) + PAD


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
    totals, variable = compute(q)
    values = {
        "issuer_tin": q["issuer"]["tin"],
        "issuer_address": q["issuer"]["address"],
        "issuer_website": q["issuer"]["website"],
        "quotation_number": q["quotation"]["number"],
        "quotation_date": q["quotation"]["date"],
        "project": q["quotation"]["project"],
        "valid_until": q["quotation"]["valid_until"],
        "customer_name": q["customer"]["name"],
        "customer_address": q["customer"]["address"],
        "customer_contact_name": q["customer"]["contact_name"],
        "customer_contact": q["customer"]["contact"],
        "currency": q["currency"],
        "vat_label": "VAT Excl." if q["vat"]["basis"] == "exclusive" else "VAT Incl.",
    }

    def substitute(paragraph, mapping):
        # Assign only runs holding a placeholder: setting run.text drops drawings.
        for run in paragraph.runs:
            text = run.text
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
    for item in q["items"]:
        row = copy.deepcopy(proto)
        proto.addprevious(row)
    proto.getparent().remove(proto)
    for row, item in zip(items.rows[1:-1], q["items"]):
        qty = f"{item['quantity']:,f}".rstrip("0").rstrip(".")
        mapping = {
            "item_no": item["no"],
            "item_title": item["title"],
            "item_detail": item["detail"],
            "unit_price": item["note"] or money(item["unit_price"]),
            "quantity": f"{qty} {item['unit']}".strip(),
            "line_total": "Variable" if item["line_total"] is None else money(item["line_total"]),
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
    lines = total_lines(q, totals, variable)
    for n, (label, amount) in enumerate(lines):
        for source, text in ((label_run, label), (amount_run, amount)):
            run = copy.deepcopy(source)
            label_run.addprevious(run)
            run_obj = type(total.runs[0])(run, total)
            run_obj.text = ("\n" if n and source is label_run else "") + text
    label_run.getparent().remove(label_run)
    amount_run.getparent().remove(amount_run)
    resize_item_frame(d, q["items"], lines)

    remark = next(p for p in d.paragraphs if "{{remark}}" in p.text)
    for text in [*q["remarks"], q["payment_terms"]]:
        new = copy.deepcopy(remark._p)
        remark._p.addprevious(new)
        for t in new.iter(f"{W}t"):
            t.text = t.text.replace("{{remark}}", text)
    remark._p.getparent().remove(remark._p)

    pairs = list(signs.rows)
    issuer, customer = q["signatories"]["issuer"], q["signatories"]["customer"]
    count = max(len(issuer), len(customer))
    protos = [r._tr for r in pairs]
    for n in range(count):
        line, name = (copy.deepcopy(p) for p in protos)
        protos[0].addprevious(line)
        protos[0].addprevious(name)
    for p in protos:
        p.getparent().remove(p)
    rows = list(signs.rows)
    for n in range(count):
        line, name = rows[2 * n], rows[2 * n + 1]
        for col, people in ((0, issuer), (1, customer)):
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
    return totals, variable


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
        totals, variable = fill(q, args.template, args.output)
    except (InputError, json.JSONDecodeError) as exc:
        print(f"Cannot fill quotation:\n{exc}", file=sys.stderr)
        return 2
    report = {
        "output": str(args.output),
        "lines": [
            {
                "item": i["no"],
                "charge": i["charge"],
                "line_total": None if i["line_total"] is None else str(i["line_total"]),
            }
            for i in q["items"]
        ],
        "totals": [{k: str(v) for k, v in t.items()} for t in totals],
        "variable_items": variable,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
