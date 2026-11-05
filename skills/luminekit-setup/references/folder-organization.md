# Recommended company work folder organization

Offer this when a work folder holds company business records and the user asks for an organization or has no clear one. The user's current structure has priority: adopt what already works, recommend only the parts that solve a real problem, and record the chosen version in their knowledge folder. Nothing moves during setup; reorganizing existing files is a migration.

## Top-level areas

```text
projects/<client>/<engagement>/
internal/<company>/<concern>/
external/<company>/<concern>/
library/<kind>/
```

| Area | Holds | Example concerns |
| --- | --- | --- |
| `projects` | Customer engagements, one home per engagement under its client. Shared client material uses `projects/<client>/account/`; our own initiatives use `projects/<our-company>/<initiative>/`. | — |
| `internal` | Administration of our own companies, one folder per legal entity. | `registration`, `tax`, `banking`, `finance`, `hr`, `governance`, `procurement/<case>` |
| `external` | Records about outside companies: customers, suppliers, partners. | `registration`, `tax`, `profiles`, `banking` |
| `library` | Reusable material not tied to one engagement. | `templates`, `policies`, `examples`, `products`, `research` |

The knowledge folder and the hidden `.agent-workspace` scratch folder chosen during setup sit beside these areas.

## Placement rules

- File by the company a record is about, not whose form was used. Keep distinct legal entities in separate folders.
- A customer's registration or vendor profile goes in `external/<client>/`; its engagements go in `projects/<client>/`. Use the same folder name in both, matching the ID in the knowledge index.
- Purchases for a specific customer delivery stay with that engagement. Internal purchases go in the buying company's `internal/<company>/procurement/<case>/`.
- A filled document is an example, not a blank template.
- Reference a record from another place instead of copying it.

## Inside an engagement

Files can sit directly in the engagement folder; names following the [naming defaults](naming-defaults.md) already say what each file is. Add document-type folders once a flat list is hard to scan, starting with the ones that have files: `quotations`, `agreements`, `billing`, `delivery`, `meetings`. Add others such as `approvals`, `design`, `plans` or `reports` when real files need them. Inside `billing`, group by real cases such as `subscription/year-1/` or `sow/m03/`.

## Avoid

- Folders by state or version, such as `final/`, `signed/` or `old/`; the state belongs in the file name.
- Folders by file format, such as all PDFs or all contracts in one place.
- Empty placeholder folders and year layers by default. Closed projects stay where they are, and the knowledge index records that they are closed. A long-running area such as `internal/<company>/finance` can add years once it holds many files.

Folder names are lowercase with hyphens.
