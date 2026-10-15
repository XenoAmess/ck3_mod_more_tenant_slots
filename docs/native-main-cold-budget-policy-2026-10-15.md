# MAIN/COLD future runtime budget policy

Observation machine: `bf-202609141645-5434332d4d`; recorded at `2026-10-15T14:12:36.282699+00:00`.

Future `native-october-reported-bugs` and `native-cold-reload` cases use a 21600-second hold and a 25200-second overall timeout. Readiness remains 1800 seconds, each command 300 seconds, polling 0.5 seconds and the normal Quit reserve 900 seconds. The product catalog and adapter exact contract checks use the same values.

R21 demonstrated that its 7200-second hold did not cover the actual operator time needed for a fresh Robert game. Its original results remain RED; no continuation is admitted because no SAVE was written and normal Quit was not qualified. This budget change supplies no business, normal-exit or release credit. The next MAIN attempt uses the existing fresh-game route.

The historical `native-legacy-v10-edit` case retains its declared 7200/10800-second hold/timeout. Its adapter now owns those budget constants rather than importing MAIN/COLD values, so the existing legacy catalog remains valid.

Runtime007, its frozen Python/native bytes, historical allocated argv and past receipts are unchanged. New attempts must run public prepare and plan again: earlier prepared cases and allocated contexts retain their original budget and adapter/catalog pins and must not be reused after this change. New prepare, full-host static preflight and allocation remain separate from launching a game.

Validation covers both cases through public Selection, including all five generated budget flags and the 900-second Quit reserve. Negative checks reject previous/mixed hold/overall values and changes to readiness, command or polling budgets. Existing adapter tests exercise fixture preparation, product-only cold preparation, actual origin matching and evidence rejection. Legacy regression checks ensure its independent budget still matches its public route.

Ownership: these are MTS case/operator budgets, so the change belongs to this product. The framework already supports these explicit values and supplies the global readiness floor; no new framework policy or runtime fork is needed.

Actual offline validation: native adapter 7/7 PASS; legacy adapter 10 PASS and 1 explicit-input full-host test SKIPPED. Both Python processes returned 0 against selected runtime007 source. Process receipts: `artifacts/bugfix-20261015/future-main-cold-budget-tests-001/`. No game was started. A new real-product prepare/full-host static preflight is still required before R22 allocation.
