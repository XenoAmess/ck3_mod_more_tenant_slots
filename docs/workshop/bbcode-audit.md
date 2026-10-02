# Workshop BBCode and Change Notes audit — v10

Product: `more_tenets_slots_xa_dev`; existing Workshop item **3182367229**. This package prepares publication copy; it does not claim an upload, media replacement, or public read-back has happened.

## Anonymous public baseline

[baseline.json](baseline.json) records an anonymous `GetPublishedFileDetails` response fetched at `2026-10-02T19:22:58.169161+00:00` (HTTP 200, item result 1). Public visibility was `0`, banned was `0`, title was `more_tenets_slots_xa_dev`, and tags were `1.16 'Chamfron'` and `Religion`. The previous description is preserved verbatim, including CRLF, with 592 UTF-8 bytes and SHA-256 `3ca1ede9369ee68e73333043bc2fc43c9264e9d0cd2b1524a0812dd0c80880f8`. The old preview CDN URL and numeric upload timestamp are retained for later comparison.

The API does not expose the previous uploaded descriptor version, source commit, or tag. Repository pre-migration version 9 / CK3 1.19.0 is a local source baseline, not proof of the last public content version. The final release changelog must distinguish those facts.

## Findings and revisions

| Finding | Revision | Evidence / publication action |
| --- | --- | --- |
| `tenant` and `number ot` misspellings; repeated unstructured links | Use `tenet`, supported Steam BBCode headings/lists and named links | [description.bbcode](description.bbcode); nesting checked |
| No explanation of the new rite system or GUI | Describe rite creation and faith grids, scrolling, and slot-100 selector repair | [Migration report](../migration-report.md), [R0009](../live-R0009-final-source.md) |
| Slot count could imply 100 valid tenets | Retain native restrictions, conflicts, costs and DLC requirements; no claim of 100 compatible tenets | Original definitions inherited |
| No empty-slot explanation | Describe two real tenets with trailing empty slots and compatible tenets with intervening gaps; retain native tenet/doctrine eligibility | R0009/R0010 two-tenet save/reload; [R0012](../live-R0012-sparse-create.md) actually created slots 1, 2, 3, 100 with 96 gaps. R0011 corrected R0008: Absent names the incompatible Monasticism doctrine, not an empty slot |
| `DEFAULT_MAX_TRADITIONS = 10000` without test boundary | Explain base cap and limited representative coverage | R0007 tenth tradition paid and started; no completed establishment or 10000-item test |
| Stale public compatibility tag | Body identifies tested CK3 1.20.0.3 (Crozier); actual Workshop tag still needs updating | Exact version pinned in source and final live evidence |
| Old GUI media and thumbnail | Three new native rite screenshots are commit-pinned; the separate thumbnail is explicitly identified as promotional concept artwork | [Media provenance](media/provenance.json), public raw HTTP/byte checks below; Steam CDN replacement/read-back remains required |
| Language coverage and runtime claims could be conflated | List the exact nine included locales and identify non-Chinese checks as format certification; future live validation uses Simplified Chinese only | [Localization coverage](../localization-coverage.md), current AGENTS rule; historical English evidence and screenshots remain historical facts |
| Upstream attribution might be lost | Retain Holger thanks, original item 2904268802, current item 3182367229 and source repository | Old baseline and revised body |
| Compatibility could be overstated | State CK3 1.19 save migration, all DLC combinations and separate POD products are outside verified coverage; overlapping GUI mods may need a patch | Migration report; no all-log-zero claim (R0010 scene errors remain documented) |

## Validation and frozen publication text

Final local description: **4044 UTF-8 bytes**, below Steam's **8000-byte** maximum; **3241 normalized characters**, **45 lines**, **4043 normalized UTF-8 bytes**. Normalized SHA-256: `96e7059b85c42b5ab9503d0d3e443a6dc8078ce3b83018253523423088c0299f`; file SHA-256: `82a89fd848ea57eb5be45c2415a7b91f517d343fc85cffb5822362d09f52d43e`. All headings, bold, list, URL and image tags are supported and correctly nested; list item markers are checked separately. Holger attribution and source/upstream/current-item links are retained. The three image links contain the exact 40-character media commit `5be332f4bf9c4da6652b3977cbc973919861e513`.

[change-notes-v10.txt](change-notes-v10.txt) is the complete bilingual player-visible update text, frozen before submission: **2013 normalized characters**, **23 lines**, **2727 normalized UTF-8 bytes**, SHA-256 **`009a95736c0a87d7fd4db4e9bfb592594a6d4e0b60b5556cec25ea01aa837754`**. File size is **2728 bytes**; file SHA-256 is `39c1ecfa0ee2def4c7a01dcb67c27ab4b1a65167200020c5a1b601c06614c162`. Both files are UTF-8 without BOM, LF, with one final newline. These exact metrics match [publication-text-freeze-v10.json](publication-text-freeze-v10.json). Normalize CRLF/CR to LF and remove trailing newlines exactly as the framework verifier does before comparing public text. Edited text requires a new recorded freeze and audit before submission.

Claims were checked against the migration report, R0009/R0010, the nine-language format report and [R0012's native receipt](../evidence/live-R0012.json). R0012 observed nonempty zero-based indices `[0,1,2,99]`, 96 empty slots, a successful native creation at cost 5775, and piety 84700→78925. The text claims that creation, without claiming all sparse layouts or tenet combinations work. The notes include the planned Workshop media/thumbnail refresh, which must actually be published before those notes become a release claim. This audit does not require a new CK3 or `open_kaishek` run.

Follow-up evidence at commit `f5751e07870578b4105fbc0035cfc7e054870638`: [R0013](../live-R0013-cold-reload.md) records native Simplified Chinese cold loading and resaving of the R0012 binary. Its [offline text-save inspection](../evidence/live-R0013-save.json) finds actor 33339 referencing rite 153, four actual core tenets, 128 doctrines and piety 78925. That receipt is `offline-save-inspection-only`, `live_verified=false`; it inspects the game's new native text save rather than directly melting the R0012 binary. Public copy/freeze remain unchanged and do not add a separate four-tenet cold-reload claim.

## Commit-pinned media verification

All three original BBCode image URLs returned **HTTP 200**, **no redirect**, `Content-Type: image/jpeg`, and `Access-Control-Allow-Origin: *` when requested anonymously with Steam Community as the Origin. Each JPEG decoded successfully at **1920×1080**; its bytes exactly match both the local file and the blob at the pinned media commit. All are below Steam's 2 MB screenshot limit. Full URLs, byte counts, headers and digests are preserved in [bbcode-audit-v10.json](bbcode-audit-v10.json).

| Image | Bytes | SHA-256 |
| --- | ---: | --- |
| `01-rite-creation.jpg` | 458079 | `c97fb4cc4b9b4b79183f9b33df303f3576b8cdd4161f7a9f94ca8c19d67cd940` |
| `02-tenet-selector.jpg` | 510841 | `ee547aa422eddf66d4fb079157163b379f259c1a433e93f3e177cc595913c853` |
| `03-two-tenet-rite.jpg` | 529406 | `8bf1978221c06a0501b938601fbdbf79d21371a0628704b6d983bc2cdf187ddb` |

Preview review confirms that the first image shows the Simplified Chinese native creation window and blank cards, the second the native tenet selector, and the third the saved two-tenet rite. Captions match their subjects. Historical English images do not constitute new English runtime testing. Public raw availability proves source-image delivery; it does not prove Steam has saved the new body, rendered the images or replaced its media strip.

Publication completion still requires: update this existing item; confirm final description exactness via anonymous API; confirm complete notes at a unique public changelog entry ID with exact normalized characters, lines and SHA-256; verify new thumbnail/media CDN pixels and order; verify fresh subscribed content against the canonical manifest; record the published release changelog. Reuse `ck3_eternal_recurrence/tools/verify_workshop_publication.py` for public text validation.

## Ownership and framework enrichment decision

Product-specific public baseline, bilingual copy, original-author attribution, release claims and audit remain in this independent repository. The framework already documents generic BBCode byte limits, commit-pinned image rules, upload boundaries and exact Change Notes verification; this package reuses those contracts and adds no new generic behavior requiring a duplicate framework implementation. New reusable publishing failures discovered by the publication work package should be enriched there separately.
