# Configure the actual project

Read for initial setup or a requested change to project conventions. Inspect existing entries, documentation owners, native rules/memory, scripts, tests, hooks, task commands, trackers and local work before proposing locations. An adequate route needs no rewrite. Installation ends at installation; it does not authorize adoption.

## Resolve choices once

Resolve only consequential choices not already settled by the user or project. Ask together where useful, and continue independent inspection while answers are pending. A suggestion is not a selected preference. Keep dependent setup pending until the answer arrives; an explicit decline can be recorded without blocking ordinary documentation work.

- Knowledge homes and the selected OKF bundle boundaries; distinguish maintained knowledge, controlled originals, plans and disposable scratch.
- Actual reader tasks and document families. Engineering and business work are equally supported; source code is not a universal prerequisite. Use the catalog procedure of `luminekit-docs` for relevant vocabulary.
- Temporary work location. Suggest a suitable location from actual conventions; the user may choose an ignored local folder, shared/versioned plans or external scratch. There is no universal default. Use one compact entry per real initiative and create focused work owners only when useful. Existing docs must work without ignored state.
- Human attribution: if unset, ask whether the user wants attribution and which name or stable pseudonym to use as `human:<id>`. Offer omission as a valid choice. Explain that attribution does not record verification or approval. Never derive personal identity from accounts, Git or the home directory. Ask about conflicting saved aliases before replacing either.
- Harnesses actually used. Keep one substantive convention owner and thin native pointers where supported. File presence does not establish automatic loading; observe the actual host separately. Do not assume one harness loads another's instruction or memory files.

## Establish the selected setup

For authorized application:

1. Record the maintained knowledge homes, actual bundle boundaries and selected workspace in the existing project convention owner. Inspect a destination before creating or reusing it. Make the selected workspace usable with a compact entry describing its purpose and real initiative routes; an existing useful entry needs no rewrite. Explain local ignored versus shared/versioned work and apply only the selected ignore policy. Create initiative owners when real work needs them, without empty future stages. An external workspace is valid; do not create a second default directory.
2. Establish or reconcile a small Markdown catalog using the catalog procedure of `luminekit-docs`. Record used types, tags, attribution conventions and source/lifecycle choices with their meanings and examples. An existing convention page can own this catalog; a separate file is useful only when it serves a distinct reader task. Keep it with maintained guidance, reachable without ignored scratch. Preserve native writer vocabulary and actual deterministic lookup contracts.
3. Record the exact selected human actor alias or explicit omission preference in the project convention owner, then add [instruction routes](#instruction-routes) to it.
4. Record agent attribution as a convention: agents/tools use the actual known `<producer>/<version>`, processes use `process:<id>`. Resolve event identities from reliable runtime information rather than fixing the current model as every future writer. Keep machine actors distinct from the user's alias; requesting or accepting work does not verify it. If the actual identity is unavailable, omit the optional family rather than inventing a version.

## Instruction routes

Conventions, knowledge locations, naming, workspace and attribution belong in documentation, never in agent instruction files. The canonical instruction file holds a short route that tells an agent where to start, for example "Before working here, read `docs/index.md`; it records this project's conventions and where knowledge lives."

- Keep one canonical instruction file for each directory scope. Use the established owner, such as `AGENTS.md` or `CLAUDE.md`, and put the documentation route there once. When none exists, create `AGENTS.md` at the project or folder root.
- When both files exist or multiple harness entrypoints are needed, consolidate shared instructions in the canonical file and make the other files thin imports or explicit routes to it. For example, with canonical `AGENTS.md`, `CLAUDE.md` contains `@AGENTS.md`. If `CLAUDE.md` is canonical, route `AGENTS.md` to it using an explicit instruction to read `CLAUDE.md`; use native import syntax only where the consuming harness supports it. Keep routes one-way and free of cycles.
- Preserve unique existing rules when consolidating; resolve conflicting rules before replacing either source. Keep genuinely harness-specific rules in their native entrypoint only when needed, without repeating shared instructions. Nested instructions for a different directory scope remain distinct.
- Tell the user which files were created or changed. File presence does not establish automatic loading; observe the actual host separately.

Preserve choices on rerun. A later category addition updates the small catalog without another setup interview. New producer-defined fields are outside ordinary setup; use standard OKF fields and Markdown first. Existing unfamiliar fields remain preserved.

## Check the result

Read back the instruction entries, catalog and workspace route as a new reader would. Check that each entrypoint reaches the same canonical instructions for its scope without duplicated rules, broken imports or cycles, aliases agree, the chosen directory is usable, local links reach substantive owners and ordinary guidance has no required ignored-work dependency. Deliver each actual location and unresolved choice. If awaiting answers, leave that part explicitly pending rather than calling setup complete. A plan-only request produces the same concrete choices/destinations as a proposal without writes.

When usable orchestration and the user's workflow make preferences relevant, preserve or offer provider/model/options intent. Check proposed choices against current capabilities; keep project role preferences separate from machine-local identifiers and secrets. Follow the independent-runs procedure of `luminekit-arena` and current host instructions for actual dispatch; configuring preferences does not authorize or demonstrate a panel. Single-harness projects need no orchestration setup.

Consumer support is guidance through skills. Do not generate validator installations, CI, hooks, schema registries, indexing services or an application as part of setup. Existing project checks remain applicable. A materially different tooling request has its own scope.

For authorized moves, use the migration/application procedure of `luminekit-docs`: inventory consumers before moving, retain recoverable current bytes and unique open value, repair incoming routes, verify destinations before retiring originals. Preserve conflicts explicitly. No Git tag, commit, global memory copy or bulk migration follows merely from setup.
