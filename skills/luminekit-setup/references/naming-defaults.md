# Recommended file naming defaults

Offer these when a user wants a naming convention for new business files. They are defaults, not rules: the user can adopt, change or drop any part, and their existing conventions win. Record the chosen version in their knowledge folder. Existing files are renamed only when the user asks for a migration.

## Pattern

```text
Order [Issuer] Counterparty Subject Document-Type Official-ID Revision REPRESENTATION (Date) [State].ext
```

Issuer and state keep literal square brackets and the date keeps literal parentheses in the actual name; the other fields are plain words. Subject and document type are always required. Issuer is required on any issued or received document; an unissued working source can leave it out. Every other field is optional: leave out a field the user cannot support instead of filling it with a placeholder. Use readable words with spaces and normal capitalization, and keep other languages, acronyms and official identifiers as they are.

| Purpose | Example (synthetic) |
| --- | --- |
| Working source | `Example Bank Printer Lease Quotation (20261013).docx` |
| No established date | `Example Bank Printer Lease Quotation.docx` |
| Draft sent for review | `[Our Company] Example Retail Support MSA v0.1 (20260101) [For Review].docx` |
| Redline of a later revision | `[Our Company] Example Retail Support MSA v0.2 REDLINE (20260115) [For Review].pdf` |
| Signed agreement | `[Our Company] Example Retail Support MSA (20260101) [Signed].pdf` |
| Quotation signed by both sides | `[Our Company] Example Bank Printer Lease Quotation (20261013) [Signed].pdf` |
| Received supplier offer | `[Supplier Co] Our Company Scanner Quotation Q-2025-0171 v3 (20250616).pdf` |
| Personal identity document | `[Example Immigration Bureau] Alex Example Tourist Visa (Valid 20250904-to-20251204).pdf` |
| One side of a card | `[Example Transport Office] Alex Example Driver License FRONT.jpg` |
| Member of an ordered submission packet | `06 [Example Immigration Bureau] Alex Example Alien Registration Card.pdf` |
| Lease signed only by the tenant | `[Example Landlord] Alex Example Apartment Lease (20260512-to-20270511) [Partially Signed].pdf` |

- **Issuer:** the legal entity that issued the document, first and in brackets. A received document keeps its real issuer; receiving or reviewing it does not make us the issuer.
- **Counterparty:** the addressed customer, supplier or subject company, using one consistent display name. For a personal document such as a passport, degree or visa, this is the holder.
- **Order:** a two-digit prefix such as `06` only for members of a packet that must be submitted in a set order. It comes before everything else.
- **Subject and document type:** what it is about and what it is, such as `Printer Lease Quotation` or `Support MSA`. For commercial documents, name the governing agreement rather than a loose category.

## Official IDs, revisions and representations

- Keep official numbers exactly, including leading zeros and punctuation. When an ID could be mistaken for a date, add a role word: `Invoice No. 20260001`. A filename convention never replaces the company's own numbering system.
- If an ID contains a character that file names cannot hold, record its exact value in the knowledge folder and note how the file name renders it.
- Revisions use a `v` prefix: `v0.1`, `v0.2` for drafts, or the issuer's own revision label for a received document (`v3`). A signed copy usually drops the revision unless several signed copies must be told apart.
- A distinct representation of the same revision is an uppercase word after the revision, such as `REDLINE` or `CLEAN`, or a part of the same document, such as `FRONT`, `BACK` or `PAGE 2`.

## Dates

- Use the date that matters for the document type: issue date for a quotation or invoice, revision date for a negotiation draft, covered period for a certificate. Effective, signature, received and coverage dates are different facts. Never use a download date or file modification time.
- `YYYYMMDD` when the day is known, `YYYYMM` for a month, `YYYY` for a year or edition, `YYYYMMDD-to-YYYYMMDD` for a period. With no established date, leave the date out.
- Name an alternate date basis in words inside the parentheses: `(Effective 20261013)`, `(Received 20261013)`, `(Approved 20261013)`, `(Valid 20250904-to-20251204)` for a permit or visa validity period.

## State

- Use at most one state, last before the extension: `[Draft]`, `[For Review]`, `[Issued]`, `[Partially Signed]` or `[Signed]`. A review marker shows purpose, not approval. `[Issued]` suits a final document that carries no signatures, once the user confirms it was issued.
- A state needs evidence. `[Signed]` means every required signature is present on a complete copy; a single signature, receipt stamp or inherited `FINAL` label is `[Partially Signed]` or no state at all.
- Do not repeat `Signed` elsewhere in the name.
- A signed state says nothing about current applicability or payment; a later amendment does not undo an earlier signed copy.
