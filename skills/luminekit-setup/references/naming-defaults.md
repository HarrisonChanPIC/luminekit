# Recommended file naming defaults

Offer these when a user wants a naming convention for new business files. They are defaults, not rules: the user can adopt, change or drop any part, and their existing conventions win. Record the chosen version in their knowledge folder. Existing files are renamed only when the user asks for a migration.

## Pattern

```text
Subject Document-Type [Official ID] [Date] [Counterparty] [Issuer] [Revision] [Status].ext
```

Fields in brackets are optional; only the issuer and status keep literal brackets in the actual name. Leave out a field the user cannot support instead of filling it with a placeholder. Use readable words with spaces and normal capitalization, and keep other languages, acronyms and official identifiers as they are.

| Purpose | Example (synthetic) |
| --- | --- |
| Working source | `Printer Lease Quotation 20261013 Example Bank.docx` |
| No established date | `Printer Lease Quotation Example Bank.docx` |
| Issued final copy | `Printer Lease Quotation 20261013 Example Bank [Our Company] [F].pdf` |
| Revision sent for review | `Support Renewal Quotation 20261028 Example Retail [Our Company] v02 Redline [For Review].pdf` |
| Received supplier offer | `Scanner Quotation Q-2025-0171 20250616 Our Company [Supplier Co] v3.pdf` |

- **Subject and document type:** what it is about and what it is, such as `Printer Lease Quotation` or `Support Statement of Work`. For commercial documents, name the governing agreement rather than a loose category.
- **Issuer:** the legal entity that issued the document, in brackets. A received document keeps its real issuer; receiving or reviewing it does not make us the issuer. An ordinary working source can leave it out.
- **Counterparty:** the addressed customer, supplier or subject company, using one consistent display name.

## Dates and official IDs

- Use the date that matters for the document type: issue date for a quotation or invoice, revision date for a negotiation draft, covered period for a certificate. Effective, signature, received and coverage dates are different facts. Never use a download date or file modification time.
- `YYYYMMDD` when the day is known, `YYYYMM` for a month, `YYYY` for a year or edition, `YYYYMMDD-to-YYYYMMDD` for a period. With no established date, leave the date out.
- Name an alternate date basis in words: `Effective 20261013`, `Received 20261013`, `Approved 20261013`.
- Keep official numbers exactly, including leading zeros and punctuation, before the date. When an ID could be mistaken for a date and no date follows, add a role word: `Invoice No. 20260001 Example Retail.pdf`. A filename convention never replaces the company's own numbering system.
- If an ID contains a character that file names cannot hold, record its exact value in the knowledge folder and note how the file name renders it.

## Revisions and status

- Revisions use `v01`, `v02` and so on, with a word for a distinct representation such as `Redline` or `Clean`.
- Use at most one status, last before the extension: `[Draft]`, `[For Review]`, `[Issued]`, `[Partially Signed]`, `[Executed]` or `[F]` for the confirmed final copy. A review marker shows purpose, not approval.
- A status needs evidence. A contract or accepted quotation is final only when every required signature is present on a complete copy; a single signature, receipt stamp or inherited `FINAL` label is not enough. Other documents can be marked final when the user confirms it.
- Final names drop a redundant `Signed` word. Keep signing dates and representation words that distinguish copies.
- Finality says nothing about current applicability or payment; a later amendment does not undo an earlier final copy.
