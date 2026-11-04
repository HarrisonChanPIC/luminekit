# Python diagnostic evidence

Python imports can create bytecode caches; disable bytecode writes when needed for a read-only check.

For process tests, record the actual start method and distinct worker identities. Use importable worker entry points and the existing main guard rather than assuming platform defaults. The official [multiprocessing documentation](https://docs.python.org/3/library/multiprocessing.html) describes those interpreter-specific behaviors; the verification procedure of the `luminekit-engineering-change` skill owns the coordination claim.

For SQLite, inspect actual schema, connection/transaction behavior, committed rows, uniqueness/conflict handling and each returned identity. An exception or warning alone does not decide the contract outcome. Consult the official [sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) for the selected operation.
