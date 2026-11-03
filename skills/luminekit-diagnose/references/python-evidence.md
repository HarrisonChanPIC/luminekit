# Python diagnostic evidence

For read-only investigation, account for bytecode caches, logs and database effects from diagnostic code; disable or redirect writes into the permitted scope.

For process tests, record the actual start method and distinct worker identities. Use importable worker entry points and the existing main guard rather than assuming platform defaults. The official [multiprocessing documentation](https://docs.python.org/3.14/library/multiprocessing.html) describes those interpreter-specific behaviors; the shared [engineering verification procedure](../../luminekit-engineering-change/references/verification.md) owns the coordination claim.

For SQLite, inspect actual schema, connection/transaction behavior, committed rows, uniqueness/conflict handling and each returned identity. An exception or warning alone does not decide the contract outcome. Consult the official [sqlite3 documentation](https://docs.python.org/3.14/library/sqlite3.html) for the selected operation.
