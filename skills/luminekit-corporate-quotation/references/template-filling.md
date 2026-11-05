# Fill the quotation template

Read when a quotation document is needed. [The template](../assets/quotation-template.docx) is the company cover quotation with its customer, items, prices and dates left blank. It carries the UNI-PIPC logo, so a quotation issued by another entity needs that entity's approved template; ask before using this one. Detailed schedules, such as specifications, service levels and exclusions, are not part of the template. Prepare them separately when the offer needs them, and reference them in a remark.

## Present the offer

Offers charge in many ways: one-time fees, monthly or yearly fees, phased rates, down payments credited later, milestones, per-site or per-unit prices, index-linked adjustments. The script does not model any of them. Decide how the offer reads, work out every amount yourself, and give the script the values to display:

- One item row per line the customer should see, with the unit price, quantity and total that fit that line. A row can leave any of them empty, such as a down payment with only a total. A non-numeric value, such as `CPI + 2%`, `Variable` or `Included`, is shown as written.
- The totals box under the items holds whatever summary fits the offer: a contract total, separate one-time and recurring totals, VAT lines, or a note such as how a down payment is credited. Show VAT amounts only when the user wants them.
- Keep the presentation of a comparable previous offer for the same customer when the user points to one, but take every value from the current terms.

Check every amount against an independent calculation using the artifacts procedure of the `luminekit-workflow` skill, including totals that combine rows.

## Collect the inputs

Ask the user for each value or take it from their recorded pages. Never borrow a value from another customer's offer, and confirm time-sensitive facts such as the VAT rate, prices and validity before filling. Write a JSON input file in the agent's temporary work location:

```json
{
  "issuer": {"tin": "…", "address": "…", "website": "…"},
  "customer": {"name": "…", "address": "…", "contact_name": "…", "contact": "…"},
  "quotation": {"number": "…", "date": "…", "project": "…", "valid_until": "…"},
  "currency": "PHP",
  "vat_basis": "exclusive",
  "items": [
    {"title": "Down payment on contract signature", "total": "300000"},
    {"title": "Year 1 monthly", "detail": "…", "unit_price": "50000", "quantity": 12, "total": "600000"}
  ],
  "summary": [
    {"label": "The down payment applies from Year 2 onward."},
    {"label": "Five-year total: ", "amount": "PHP 3,000,000", "suffix": " (VAT Exclusive)"}
  ],
  "signatories": {"issuer": [{"role": "…", "name": "…"}, {"role": "…", "name": "…"}], "customer": [{"role": "…", "name": "…"}]}
}
```

- Amounts are strings or integers, never floats. Numeric item amounts are formatted with thousands separators and at least two decimals. When a row's unit price, quantity and total are all numeric, the script checks that they agree.
- `vat_basis` (`exclusive` or `inclusive`) labels the price columns, such as "(PHP, VAT Excl.)". Without it the columns show only the currency.
- Each `summary` line has a `label`, a bold `amount` and a `suffix`, any of which can be left out. They are shown exactly as written.
- `detail`, `unit`, `no`, the customer's address and contact fields, and `summary` are optional. Leave out what the user did not give instead of inventing it.
- Our side always signs with two signatories, so `signatories.issuer` needs exactly two people with their roles; the script refuses one or three. The customer side needs at least one.

## Remarks

Unless the input gives `remarks`, the script writes the company's standard remarks, in this order:

1. The amounts stated in this quotation are in {currency name} ({currency}) and are exclusive of taxes (inclusive for an inclusive VAT basis). This quotation shall remain valid before {valid_until}.
2. This quotation shall become effective only upon signature by the authorized signatories.
3. Upon acceptance and return of the signed quotation by the Customer, the quotation shall be deemed a reservation. The Customer shall ensure that the signatory is duly authorized to sign on behalf of the Customer.
4. Any terms and conditions not specified in this quotation shall be governed by the master agreement (the "Agreement") to be entered into subsequently by the parties. In the event of any inconsistency between the terms and conditions of this quotation and those of the Agreement, the terms and conditions of the Agreement shall prevail.
5. Any `extra_remarks`, such as a reference to a separate schedule.
6. Payment Terms: As stipulated in the Agreement.

Keep these unless the user or the offer calls for something else.

- The standard remarks need `quotation.valid_until` and `vat_basis`. The currency name is known for PHP, USD and TWD; give `currency_name` for any other code.
- Clause 4 assumes a master agreement will follow. When none will, set `"master_agreement": false`: clause 4 is left out and `payment_terms` becomes required. Ask the user which applies when the offer does not say.
- `payment_terms` replaces the default "As stipulated in the Agreement." text, for example with milestone payments.
- To change or drop a standard clause, give `remarks` as the complete list instead. It is used exactly as written, so start from the standard wording above and edit only what the offer needs.

## Fill and check

Run [the fill script](../scripts/fill_quotation.py) with `uv`, which installs its declared dependency:

```sh
uv run scripts/fill_quotation.py input.json "Quotation.docx"
```

The script refuses missing or invalid inputs and lists every problem. Ask the user for those values before filling; never pass placeholder text such as "TBC" to get past the check. It never overwrites an existing file. Its JSON output echoes the displayed items, summary and remarks, and says which rows it checked arithmetically.

Open the result in Word, or render it with LibreOffice (on macOS `soffice` is inside `LibreOffice.app/Contents/MacOS`), and check its layout. Quick Look previews misplace the rounded frames. The item table's rounded frame is resized from an estimate, so check that it still encloses the table and totals. The quantity column is narrow: leave out a unit the item title already gives, such as months for a monthly fee. The filled document is a draft. Issuing, signing and sending remain separate decisions.
