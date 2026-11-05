# Fill the quotation template

Read when a quotation document is needed. [The template](../assets/quotation-template.docx) is the company cover quotation with its customer, items, prices and dates left blank. It carries the UNI-PIPC logo, so a quotation issued by another entity needs that entity's approved template; ask before using this one. Detailed schedules, such as specifications, service levels and exclusions, are not part of the template. Prepare them separately when the offer needs them, and reference them in a remark.

## Collect the inputs

Ask the user for each value or take it from their recorded pages. Never borrow a value from another customer's offer, and confirm time-sensitive facts such as the VAT rate, prices and validity before filling. Write a JSON input file in the agent's temporary work location:

```json
{
  "issuer": {"name": "…", "tin": "…", "address": "…", "website": "…"},
  "customer": {"name": "…", "address": "…", "contact_name": "…", "contact": "…"},
  "quotation": {"number": "…", "date": "…", "project": "…", "valid_until": "…"},
  "currency": "PHP",
  "vat": {"basis": "exclusive", "rate": "0.12"},
  "items": [
    {"title": "…", "detail": "…", "charge": "one-time", "unit_price": "1000.00", "quantity": 1},
    {"title": "…", "charge": "recurring", "period": "year", "price_note": "CPI + 2%", "quantity": 1, "unit": "/ yr"}
  ],
  "remarks": ["…"],
  "payment_terms": "…",
  "signatories": {"issuer": [{"role": "…", "name": "…"}, {"role": "…", "name": "…"}], "customer": [{"role": "…", "name": "…"}]}
}
```

- Amounts are strings or integers, never floats. `vat.basis` is `exclusive` or `inclusive`, and `vat.rate` is a fraction. Use `"0"` only when the user confirms there is no VAT.
- `charge` is `one-time` or `recurring`. A recurring item needs a `period` such as `year`. One-time and recurring amounts are totalled separately, and each recurring period gets its own total.
- Use `price_note` instead of `unit_price` only for a price the offer itself leaves variable, such as an index-linked adjustment. A price not yet agreed is a missing input, not a variable price. Such items show "Variable" and are excluded from the totals, and the totals say so.
- Our side always signs with two signatories, so `signatories.issuer` needs exactly two people with their roles; the script refuses one or three. The customer side needs at least one.
- `detail`, `unit` and `remarks` are optional. Payment terms become the last remark before the validity line.

## Fill and check

Run [the fill script](../scripts/fill_quotation.py) with `uv`, which installs its declared dependency:

```sh
uv run scripts/fill_quotation.py input.json "Quotation.docx"
```

The script refuses missing or invalid inputs and lists every problem. Ask the user for those values before filling; never pass placeholder text such as "TBC" to get past the check. It never overwrites an existing file. Its JSON output gives line totals and the net, VAT and gross amount for each group. Line totals round half up to cents, and VAT is computed on each group total. Check these against an independent calculation, using the artifacts procedure of the `luminekit-workflow` skill.

Open the result in Word, or render it with LibreOffice (on macOS `soffice` is inside `LibreOffice.app/Contents/MacOS`), and check its layout. Quick Look previews misplace the rounded frames. The item table's rounded frame is resized from an estimate, so with unusually long descriptions check that the frame still encloses the table. The filled document is a draft. Issuing, signing and sending remain separate decisions.
