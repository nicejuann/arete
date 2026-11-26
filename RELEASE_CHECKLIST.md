# ARETÉ v2.0 RC19 acceptance checklist

This is a release candidate, not a claim of production readiness.

## Android / installed app
- [ ] Open app and verify version 2.0-rc19.
- [ ] Read and save an article, add a note, mark it read, close and reopen.
- [ ] Change favorites, theme, text size and feed layout; restart and confirm persistence.
- [ ] Search by topic and accented name, open a result and return.
- [ ] Try a guided reading path, quiz, saved-item recall session, and visual-only discovery.
- [ ] Export a backup, then restore it on a test browser/profile; compare saved IDs, notes, books, positions, settings and review schedule. Do not overwrite real data to test.
- [ ] Once the app is installed and loaded, use airplane mode, reopen and read original articles and local diagrams.
- [ ] Import a short TXT, unencrypted EPUB and text-based PDF; verify actual text and reading position.
- [ ] Open a publisher audio/video source and test supported embedded playback.
- [ ] Verify Bible chapter fetching and offline cache. Complete integrated pack is not accepted until its publication and offline chapter navigation are confirmed.

## Release gates
- [ ] Confirm GitHub quality workflow regression and Chromium jobs succeed.
- [ ] Review link-audit output, manually inspect unavailable and unverified links.
- [ ] Complete editorial/source review of all original articles; title uniqueness alone does not establish quality.
- [ ] Complete integrated Bible build and verify actual text/edition.
- [ ] Evaluate daily use against the original purpose: voluntary learning instead of recreational scrolling.

Existing content counts at RC3 preparation: 176 originals, 48 quizzes, 20 photographic articles, 16 new-style inline diagrams, 24 distinct multimedia links, 5 guided paths. Previous imports: 42 headlines, 11 open readings, 6 museum records. No paid services required. External sources may have their own costs or restrictions. Browser/device storage can be cleared; back up personal data.

## RC3 additional acceptance
- [ ] Download the official engwebp_vpl.zip from eBible.org, import it in the Bible reader, compare several verses with eBible, and reopen in airplane mode.
- [ ] Confirm incomplete/incorrect ZIP rejection without replacing an existing offline pack.
- [ ] Confirm full archive import and download remain independent of app updates. Structural checks alone do not establish text authenticity or verse-level completeness.

## RC3 review artifacts
- [ ] Download the quality workflow artifact; inspect source-inventory.json and link-audit.json coverage.
- [ ] Complete the editorial-review.csv entries manually, recording evidence for factual corrections. The automatically created ledger is not an editorial audit.
- [ ] Verify mobile Chromium EPUB and synthetic Bible archive tests succeed. These do not prove authentic Scripture or real Android import behavior.

## RC4 editorial progress
- [x] First ten source-aligned article revisions, with dated scope and preserved IDs.
- [ ] Review remaining 16 articles, including source suitability and factual claims.
- [ ] Independently verify revised articles and actual media links.

## RC5 editorial progress
- [x] Second ten source-aligned article revisions, with dated scope and preserved IDs.
- [ ] Independently verify all revised material and remaining source links.

## RC6 editorial progress
- [x] Third ten source-aligned article revisions, with dated scope and preserved IDs.
- [ ] Independently verify revised material and archival image delivery.

## RC7 editorial progress
- [x] Fourth ten source-aligned article revisions, with dated scope and preserved IDs.
- [ ] Independently verify revised material and external links.

## RC8 editorial progress
- [x] Fifth ten source-aligned article revisions with preserved IDs.
- [ ] Verify direct access to two LOC references and independently review revised material.

## RC9 editorial progress
- [x] Sixth ten source-aligned article revisions, with all nine distinct references retrieved.
- [ ] Resolve access to LOC teachers guide for the deferred article; independently review revised content.

## RC10 editorial progress
- [x] Seventh ten source-aligned article revisions; eight distinct references retrieved; three passage-specific Scripture links.
- [ ] Independent factual review and prior unresolved LOC link.

## RC11 editorial progress
- [x] Eighth ten source-aligned article revisions; all ten original references retrieved.
- [ ] Independent factual review and prior unresolved LOC link.

## RC12 editorial and narration progress
- [x] Twenty further source-aligned revisions; direct replacement for previously deferred photo-analysis reference.
- [x] All 176 narration inputs preserved in word-boundary chunks; source syntax checks passed.
- [x] Profile reports editorial pass counts, not certification.
- [ ] Independently verify revised claims and previously blocked references elsewhere in the collection.
- [ ] Test narration on Android, including interruption, long articles and selected voice; confirm actual CI and Pages deployment.

## RC13 editorial and discovery progress
- [x] Twenty further source-aligned revisions; 120 of 176 revised.
- [x] Revised reads filter, editorial labels and backup preference simulated checks.
- [x] Browser CI runner pinned to Ubuntu 24.04 after RC12 install failure.
- [ ] Confirm RC13 browser job runs successfully, including offline and mobile-size smoke tests.
- [ ] Independent source/claim verification and actual Android acceptance.

## RC14 editorial and reading progress
- [x] Twenty further source-aligned revisions; 140 of 176 revised and none under 120 words.
- [x] Reading paragraph text-preservation and escaping checks; RC13 browser, regression and link-audit jobs passed.
- [ ] Verify RC14 workflow, actual phone reading experience, media and authentic Bible import; independently verify revised claims.

## RC15 editorial and reading progress
- [x] Twenty further source-aligned revisions; 160 of 176 revised.
- [x] Focused reading return position and reset simulated checks; RC14 browser, regression and link-audit jobs passed.
- [ ] Verify RC15 workflow, Android reading and actual multimedia; independently review claims and Bible import.

## RC16 initial editorial baseline
- [x] All 176 original articles have undergone an initial substantive editorial revision; 48 quizzes preserved.
- [x] All article IDs, titles and source URL format preserved/validated; full collection minimum 150 words.
- [x] Profile transparently reports initial editorial completion; regression baseline asserts 176 dated revision records and 48 quizzes.
- [ ] Independently verify factual claims and licensing across the entire collection, and check links/media on Android; prior pass source claims are not independently certified.
- [ ] Confirm RC16 browser, regression and link-audit results and Pages deployment.
- [ ] Evaluate real reading enjoyment, visual quality, narration, and authentic offline Bible import before stable release.

## RC17 visual acceptance
- [x] Daily edition and collection selection redesigned; SVG navigation icons and version consistency.
- [x] Simulated stability, allowed topics, focused article return and old saved data validated.
- [ ] Confirm mobile Chromium 320px viewport, theme switch, and daily feature interaction checks.
- [ ] Assess actual Android visual appeal, reading comfort and voluntary return behavior.

## RC18 visual acceptance
- [x] Six new inline explainers and dedicated visual collection; source text preserved.
- [x] Simulated visual filtering, topic restrictions, backup compatibility and media labels.
- [ ] Confirm RC18 automated browser checks and Pages deployment; evaluate physical phone display and external media.

## RC19 acceptance
- [x] Daily ranking considers explicit preferences, unread status and topic diversity.
- [x] Mocked speech lifecycle, pause/resume, stale callback and backup validation passed.
- [ ] Confirm actual browser workflow and deployment, then test Android voice quality and controls with real audio.
