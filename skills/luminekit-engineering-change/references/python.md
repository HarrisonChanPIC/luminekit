# Python implementation concerns

Follow the supported interpreter and existing runner. The standard library [unittest documentation](https://docs.python.org/3.14/library/unittest.html) describes fixtures/assertions when that is the selected framework. Keep fixtures isolated and test consequential cleanup behavior. For read-only checks, disable bytecode writes where needed and keep generated outputs inside the permitted scope.

When a contract requires exact decimal values, retain their source representation and use appropriate decimal arithmetic rather than introducing binary-floating error. The [decimal documentation](https://docs.python.org/3.14/library/decimal.html) supplies arithmetic behavior; the actual contract supplies precision and rounding policy.
