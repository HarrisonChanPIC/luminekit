# Set up a personal work folder

Read when setup is for one person's work folder rather than a software project: business documents, spreadsheets and PDFs, usually with no existing agent tooling. The aim is an agent that can find their files and keep what they tell it. Their folder organization stays as it is.

## Inspect without changing

List the top-level folders and a sample of file names to learn how the user already organizes work: by customer, project, year or document type. Note existing naming habits, a shared drive or synced folder, and files that look like controlled originals. Reading names is enough; do not open every document. Nothing moves or is renamed during setup.

## Choose with the user

Explain choices in plain language and ask together, offering a recommendation for each:

- **Where agent knowledge lives:** a small folder of Markdown pages that the agent reads and maintains, for example `agent-notes` at the top of the work folder. The user rarely needs to open it. Recommend a location inside the folder they already back up or sync.
- **Naming for new files:** offer the [recommended defaults](naming-defaults.md), and adopt the user's existing habits where they already work. Record any customization. Renaming existing files is a separate request.
- **Scratch:** where the agent keeps temporary drafts and inputs, such as a hidden `.agent-work` folder, kept apart from real documents.
- **Attribution:** whether to record a name or pseudonym on agent-written pages, as in [project choices](project-choices.md#resolve-choices-once). Omitting it is fine.
- **Instruction file:** ask whether to create one so the user's agent app finds these choices, such as `AGENTS.md` or `CLAUDE.md` in the work folder. Describe it plainly ("a short note the AI reads first"). Create it only after the user says yes; otherwise keep the choices in the knowledge folder's index and tell the user where they are.

## Create only what is real

1. Create the knowledge folder with a root `index.md` following the working-knowledge procedure of `luminekit-docs`. Add an entry for each project, customer or area the user names or that the folder clearly shows, with the names people use for it.
2. Write a page only where there is real content: what the user told you, or facts read from a document they pointed to, each with its source and date. No empty templates, placeholder pages or future sections.
3. Record the chosen conventions (knowledge location, naming choices, scratch, attribution) on one page linked from the index, and point to it from the instruction file when one exists.
4. Optionally run the fingerprint scan from the same procedure to give later duplicate and change checks a baseline, excluding the knowledge and scratch folders.

## Check and rerun

Read back the index and conventions page as a new agent would, and confirm that every native file is where it was. On a later run, keep existing choices and pages; update only what the user changes. A request to reorganize or rename existing files is a migration and follows the migration procedure of `luminekit-docs`.
