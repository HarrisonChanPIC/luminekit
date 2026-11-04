# Python implementation concerns

Follow the supported interpreter and existing runner. Keep fixtures isolated and test consequential cleanup behavior.

When a contract requires exact decimal values, retain their source representation and use appropriate decimal arithmetic rather than introducing binary-floating error. The [decimal documentation](https://docs.python.org/3/library/decimal.html) supplies arithmetic behavior; the actual contract supplies precision and rounding policy.
