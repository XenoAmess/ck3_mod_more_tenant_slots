# CK3 1.21.0 / More Tenets Slots v12 migration

Current status: **static-ready**, live acceptance and Workshop update pending. Scope is only `more_tenets_slots_xa_dev/`; the public release remains v11 until upload succeeds. Plans: [migration](migration-plan-2026-11-18.md), [acceptance](acceptance-plan-2026-11-18.md).

## Installation

`machine_id: pc-20260924rtuf-f11af23c08`. On 2026-11-18 UTC (2026-11-19 Asia/Shanghai), the framework Steam version skill selected the actual official default branch from the previously selected `1.20.0` branch. The first transport returned `No Connection`; a normal client restart using TCP for that invocation obtained actual downloads and completed installation. No game was running or launched during the update. Steam was restored offline immediately after completion and independently read back by the background probe.

- Installed launcher version: **1.21.0 (Florin)**.
- Steam build: **26757580**, StateFlags4, target/download/staging counters zero.
- EXE SHA-256: `bb3fef106240e95ecdb6f1532982e89e9432c92a99d33db623521572f06e6f79`.
- This differs from another machine's earlier 1.21.0/build26622941; that machine's ABI or acceptance is not reused as local proof.
- The nonzero historical `UpdateResult=6` remains in Steam's final manifest, while installed state and all transfer counters are complete. The successful original version-tool result is retained; the earlier failure is not rewritten.

## Reviewed native changes and implementation

All ten pinned native dependency files changed. Their exact new hashes are in [the 1.21 source contract](../dev_tools/ck3_1_21_0_sources.json); raw old/new files and complete diffs stay outside Git under the ignored task artifacts.

The two GUI files are regenerated from the new native source with the existing reversible projections: two faith tenet scrollboxes, one creation scrollbox and the existing Edit preparation action. New precepts (diet/alcohol restrictions and DLC-gated usury), naming/description generation, tenet popularity eligibility, warnings, tooltips, holy-site controls and faith interaction bindings are retained verbatim outside those changes. There are no custom replacements for the new native tenets or ordinary doctrines.

The same-name `on_rite_updated` override is regenerated from the complete new native action. In particular, the added merchant usury reputation update, `changed_tenet_status` propagation, personal-tenet fulfillment update and `has_edited_a_rite` tracking are preserved. The internal-metadata-only predicate now also requires **no changed tenet status**, so a real status update cannot be silently discarded merely because hidden selector metadata changed in the same update.

The 100 core-tenet define and council script-value mirror remain; culture inherits the current native base limit of5 (not the historical 1.20 base4). The 100 hidden inert doctrines retain zero cost/divergence and remain separate from real tenets and empty slots. New doctrine metadata schema still supports their existing fields. Native eligibility, cost, conflicts and DLC conditions are preserved.

## Verification and remaining work

The current native projection and inverse recovery pass; both actual GUI files and the full updated hook match the reviewed native input when the explicit product changes are removed. Existing selector projection2, culture-cap2 and actual tagged-build3 tests pass. Static validation checks48 release files, BOM/structure, override order, exact source identity and all nine supported languages (18 localization files,305 keys per language). Two candidate builds have identical manifests/ZIPs. These checks do not assert engine behavior or live compatibility.

The native GUI contains trailing whitespace. It is deliberately preserved by the reversible projection; the initial whole-diff whitespace check reported it. The subsequent whitespace check excludes the two exact native GUI projections, whose bytes are covered by inverse recovery, and checks all other changed files normally.

`open_kaishek` is absent from this machine's discovered workspace; its prevalidation is NOT_RUN, not a pass. Shared structural scanning is not treated as full CK3 grammar validation. The old exact-build native runtime is not repinned to this new executable. The next step is the shared public GUI-only acceptance route with an explicit native capability-gap record, followed by independent cold reload, formal tagged build, Workshop update and actual cache loading.

## Ownership

Product projections, source pins, compatibility predicate, cases and specific evidence belong here. A reusable background Steam discovery defect was fixed in the framework: interactive startup omitted optional `SILENT_STARTUP`; the actual `target_candidates` regression, all22 probe tests, full production-module strict mypy and a source/process-bound online probe passed. Framework commit `2fafef1ea76be4087725112760df8605c6816f89`; [shared record](https://github.com/XenoAmess/ck3_eternal_recurrence/blob/2fafef1ea76be4087725112760df8605c6816f89/docs/maintenance/2026-11-19-steam-interactive-context.md). This infrastructure result grants no product live or release credit.


2026-11-19：新局简中GUI业务和实际存档读回通过，正常退出及资源释放通过；独立冷载/发布尚待完成。详见 [实机报告](live-report-2026-11-19.md)。


2026-11-19：独立冷载及v12工坊发布闭环完成，包含完整公开文本读回、真实下载48文件exact match、缓存实际加载和正常退出、Steam离线及资源释放。详见[发布记录](workshop/publication-v12.md)。两项通用修复已分别提交框架；POD不在本轮结论中。
