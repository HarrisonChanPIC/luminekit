# Find and record working knowledge

Read when an agent helps someone find files or facts in their own work folder, or keeps what they tell it for later. The knowledge is for agents: people keep working in their native documents, spreadsheets and PDFs, and their folder organization stays theirs unless they ask for a change.

## Shape

Keep one small OKF bundle in the location chosen during setup, with standard fields only ([authoring](okf-authoring.md)):

- Root `index.md`: one entry per project, company, area or personal topic. Its selection description carries the names people actually use, including other-language names and useful aliases, so a request matches without opening pages.
- Focused pages: a project, a company or counterparty, recurring business facts (rates, terms, contacts), personal preferences and standing instructions. Create a page only when real content exists. An index entry alone is enough for a project with nothing more to say.
- Native files stay where they are. Pages cite their actual paths; a proposed location is labelled as proposed.

Aliases, entities, paths, tax facts and contacts are ordinary Markdown sections, not new frontmatter fields. When a page grows past one reader task, split it by task and route from the index.

## Find

Read the index, select the page or pages whose description matches, then open the native files the page cites. Search the folder directly when the index has no match, then record what was found if it will be needed again. A shared name or alias (one company with several projects, a system name used by two clients) lists the candidates; disambiguate from the request or ask, never merge. A fact that is not recorded is unknown. Do not borrow it from a similar project.

## Record

Record durable facts that change future work: a rate, term, contact, location, preference, project scope or state, or standing instruction.

- **Record and tell.** When the user states such a fact, save it to its owning page and say so in one line. The user can correct it immediately; no permission step is needed. Ask once when an instruction might be one-off rather than standing.
- **Qualify each fact** with its value, scope, source (user stated, a named document, a named email) and date. Unknown, zero and not applicable stay distinct.
- **Agent inferences are suggestions** until the user confirms them.
- **One fact, one page.** Link from other pages instead of copying.
- **Do not record** conversation summaries, session or work history, decision narratives, work logs, context that does not change future work, credentials, unrelated personal details or full email contents.
- **Superseded values** stay, with their effective period, only while they still explain existing records such as a rate used on past invoices. Otherwise replace them.

## Conflicts and staleness

A user correction updates the fact. When a document contradicts a recorded fact, show both values with their sources and dates and let the user decide. By default a signed or official document governs its own terms, and the user governs current intent and preferences.

Do not sweep for stale facts. Before a consequential output such as a quotation, invoice or formal letter, confirm time-sensitive facts with the user ("Using EWT 2% from your March note. Still right?"). Ordinary lookups use the recorded value.

## Logs

A `log.md` is optional. Create one only when its entries help a later reader, such as a dated change to a standing rate. Whenever you touch a log, remove entries that no longer help a reader. A log is never a work journal or a ritual after each edit.

## Fingerprints

[`fingerprints.py`](../scripts/fingerprints.py) (Python standard library) keeps a generated CSV of path, size, modification time and SHA-256 for a folder. Run it when the user asks or after writing files, never as a background scanner:

```sh
python fingerprints.py scan FOLDER --exclude FOLDER/<knowledge folder>
python fingerprints.py compare OLD.csv NEW.csv
```

`scan` writes `FOLDER/.fingerprints.csv` by default, rehashes only files whose size or modification time changed, and reports duplicates, moves, copies, changes, additions and deletions as JSON. It skips hidden files, Office lock files and symlinks. When anything is unreadable, it keeps the unseen entries and reports no deletions. Use `--full` to rehash everything, for example when a file may have changed without its size or timestamp changing. The hash covers file contents only, so a renamed or copied file keeps its hash.

The fingerprint file is regenerable and never edited by hand. Pages cite paths, not hashes. Identical bytes do not prove one business record: an intentional copy in two projects stays. Re-saving a document changes its bytes without changing its meaning. Finding near-duplicates needs extracted text or a semantic index, which is outside this script.
