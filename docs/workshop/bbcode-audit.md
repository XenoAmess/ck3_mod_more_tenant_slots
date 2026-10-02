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
| No empty-slot explanation | Describe two real tenets plus trailing empty slots; reject middle gaps explicitly | R0009 creation/save and [R0010](../live-R0010-cold-reload.md); R0008 middle-gap RED remains |
| `DEFAULT_MAX_TRADITIONS = 10000` without test boundary | Explain base cap and limited representative coverage | R0007 tenth tradition paid and started; no completed establishment or 10000-item test |
| Stale public compatibility tag | Body identifies tested CK3 1.20.0.3 (Crozier); actual Workshop tag still needs updating | Exact version pinned in source and final live evidence |
| Old GUI media and thumbnail | Publication work package selects new native rite GUI screenshots and rebuilds thumbnail | This copy package does not create or publish images; provenance and CDN read-back remain required |
| Upstream attribution might be lost | Retain Holger thanks, original item 2904268802, current item 3182367229 and source repository | Old baseline and revised body |
| Compatibility could be overstated | State CK3 1.19 save migration, all DLC combinations and separate POD products are outside verified coverage; overlapping GUI mods may need a patch | Migration report; no all-log-zero claim (R0010 scene errors remain documented) |

## Validation and frozen publication text

Description draft: **2746 UTF-8 bytes**, below Steam's **8000-byte** maximum; 2157 normalized characters and 29 lines. Normalized SHA-256: `9C0C08817395AD413881603F2CB6CE026924119A8698D2C1655313D1DD56DFE5`. Supported BBCode nesting is balanced, legacy misspellings are absent, and source/upstream/current-item links are retained. This draft contains no image URLs. After media is committed, the publisher may add selected commit-pinned raw image URLs, then must rerun the byte-limit/link audit and update the final description digest before upload.

[change-notes-v10.txt](change-notes-v10.txt) is the complete bilingual player-visible update text, frozen before submission: **1705 normalized characters**, **23 lines**, **2313 normalized UTF-8 bytes**, SHA-256 **`BA6E203EABFDB058FB286059A0CA95CAF7BCA2C49A424FDBB8014CDFFC092441`**. The tracked file is UTF-8 without BOM, LF, with one final newline; file SHA-256 is `DC0FDF94AEA875683AB10F084D4EFDC990CA624EE4EC6F41E382BF119F0D16DD`. Normalize CRLF/CR to LF and remove trailing newlines exactly as the framework verifier does before comparing public text. Edited notes require a new recorded freeze before submission.

Claims were checked against the migration report and R0009/R0010 evidence. The notes include the planned description/media/thumbnail refresh; the publisher must complete those actions before publishing this text. Pure documentation validation does not require CK3 or `open_kaishek` execution.

Publication completion still requires: update this existing item; confirm final description exactness via anonymous API; confirm complete notes at a unique public changelog entry ID with exact normalized characters, lines and SHA-256; verify new thumbnail/media CDN pixels and order; verify fresh subscribed content against the canonical manifest; record the published release changelog. Reuse `ck3_eternal_recurrence/tools/verify_workshop_publication.py` for public text validation.

## Ownership and framework enrichment decision

Product-specific public baseline, bilingual copy, original-author attribution, release claims and audit remain in this independent repository. The framework already documents generic BBCode byte limits, commit-pinned image rules, upload boundaries and exact Change Notes verification; this package reuses those contracts and adds no new generic behavior requiring a duplicate framework implementation. New reusable publishing failures discovered by the publication work package should be enriched there separately.
