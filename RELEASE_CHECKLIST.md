# ARETÉ v2.0 RC24 acceptance checklist

This is a release candidate, not a claim of production readiness.

## Android / installed app
- [ ] Open app and verify version 2.0-rc24.
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

## RC20 acceptance
- [x] Eight catalog-linked human recordings; on-demand player and source fallback.
- [x] Local book section selection, search and continuation; old pagination preserved.
- [ ] Verify RC20 CI and actual audio streaming, physical Android and authentic Bible import.

## RC21 acceptance
- [x] Eight new source-aligned original articles and quizzes, 184 originals / 56 quizzes; prior articles preserved.
- [x] New collection and connection-status checks in simulation.
- [ ] Confirm RC21 browser offline test and deployment; verify actual device behavior and independently review all content.

## RC22 acceptance
- [x] Six new originals and quizzes; three new learning paths and continuation controls.
- [x] Syntax, content integrity and simulated guide progress checks.
- [ ] Confirm CI, deployment and physical Android experience; independently verify claims and media.

## RC23 acceptance
- [x] 200 originals and 72 quizzes; previous content preserved.
- [x] Local quiz answer persistence, explicit retry and validated optional backup field.
- [ ] Verify CI, deployment, physical Android acceptance and independent factual review.

## RC24 acceptance
- [x] Matching release markers and worker version checks, cached navigation, previous cache retention, explicit activation.
- [x] Mocked install failure/activation/shell coherence; 200 articles and 72 quizzes unchanged.
- [ ] Confirm RC24 CI and live RC23→RC24 upgrade on physical Android. External audio, authentic Bible and independent content review remain open.

## RC25 acceptance
- [x] RC24 actual artifact inspected; previous deployment and three quality jobs passed.
- [x] Historical audit status and alternate reference links; 200 original article records preserved.
- [x] JavaScript syntax and simulated status/alternate source tests.
- [ ] Run updated audit self-test and CI; verify physical Android update, actual audio and authentic Bible; independent claim/license review remains outstanding.

## RC26 acceptance
- [x] RC25 deployment and automated jobs passed.
- [x] Exact preceding-release upgrade test added, update UX hardened, article records unchanged.
- [ ] Confirm RC26 upgrade browser test and deployment; test on physical Android and verify authentic media/Bible and claims.

## RC27 acceptance
- [x] RC26 automated and deployment results passed, including exact preceding-release upgrade.
- [x] Both parsers updated for explicit empty references and line diagnostics; JavaScript synthetic regression passed.
- [ ] Confirm official eBible archive build and artifact; verify actual text in Chromium and on Android before calling the Bible complete.

## RC28 acceptance
- [x] RC27 release and cross-version checks passed; Bible build log isolated JAM alias failure.
- [x] Explicit JAM alias, unknown-code preflight and synthetic JavaScript regression.
- [ ] Official-source build, authentic Chromium download/import and publishing; verify real Android and remaining content/media.

## RC29 acceptance
- [x] RC28 genuine archive structurally validated; source fingerprint recorded.
- [x] RC28 release quality and deployment passed.
- [x] Corrected Faith test setup and added optional Library preferences shortcut.
- [ ] Confirm authentic Chromium download, offline reading, ZIP import and publication; physical Android acceptance.

## RC30 acceptance
- [x] RC29 official source structure verified again; browser failure isolated to ambiguous test navigation.
- [x] Fix narration dispatch; verify full-text segmentation across 200 articles.
- [ ] Confirm actual browser click tests, full authentic Bible acceptance and publication, Android testing.

## RC31 acceptance
- [x] Correct fresh reader default mismatch and add chapter-heading and canonical-boundary assertions.
- [x] Bound individual chapter network requests and correct source attribution.
- [ ] Confirm RC31 regression, actual browser upgrade, genuine Bible download/import, deployment and Android acceptance.

## RC32 acceptance
- [x] Prepared complete Bible pack committed to main.
- [x] Direct Scripture reference navigation and verse-range highlighting implemented; parser and authentic offline browser assertions added.
- [ ] Confirm RC32 regression, offline reference jump and exact preceding-release upgrade, deployment, physical Android and independent editorial verification.

## RC33 acceptance
- [x] Add accessible narration segment navigation and progress indicator.
- [x] Test paused seeking, stale callback protection, progress and boundary behavior with mocked speech.
- [ ] Verify actual Chromium interaction and narrow screen layout, release upgrade and deployment, Android and real audio quality.

## RC34 acceptance
- [x] Implement per-article local narration progress, restart and completion clearing.
- [x] Add content-version guards and backup integration; add simulated resume tests.
- [ ] Confirm Chromium reload/resume, narrow dock layout, CI upgrade, deployment, physical Android and actual audio quality.

## RC35 acceptance
- [x] Implement weighted, word-aware discovery search and clear empty-result recovery.
- [x] Test relevance, prefixes, accents, multi-word matching and false-positive rejection.
- [ ] Confirm full Chromium search behavior, upgrade, deployment and physical device testing.

## RC36 acceptance
- [x] Add connected discoveries, reason labels and finite recommendations in focused reading.
- [x] Test deterministic ranking, filtering, deduplication and recommendation bounds.
- [ ] Confirm Chromium navigation, upgrade, deployment and actual relevance through editorial review.

## RC37 acceptance
- [x] Four extended originals and two new curated paths; original 200 article records preserved.
- [x] Verify sequential IDs, unique titles, minimum depth, quiz structure and numerical examples.
- [ ] Confirm complete regression, browser acceptance, independent editorial verification and live deployment.

## RC38 acceptance
- [x] Focused reader layout, direct size controls, visible reflection and depth labels.
- [x] Verify all article text and explicit paragraph breaks preserved; validate JavaScript syntax.
- [ ] Verify actual mobile rendering, font-size controls, theme contrast, upgrade and deployment in browser and Android.

## RC38 regression maintenance
Corrected stale guide-count expectation from 8 to 10. Executed the complete JavaScript release test script using an isolated V8 harness with compatible mocked VM, filesystem, URL and Fetch interfaces; 75 assertions across 32 reported groups passed. This is not native Node or Chromium CI, nor physical-device or deployment verification. No application files or content changed.

## RC38 browser acceptance repair
Actual GitHub Actions run 45916405821: native Node regression and Python Bible builder self-test passed; link audit passed (200 of 294 eligible URLs checked: 175 reachable, 0 confirmed unavailable, 25 unverified); Chromium reached line 191 before failing because the test still expected RC30 cache and HTML markers. The browser test now derives the expected build from the checked-out HTML and confirms cache existence without creating it. Offline checks verify the exact build and latest permitted article dynamically. Upgrade test was skipped in that run. Pages deployment succeeded in run 45916404927. Fresh browser/upgrade results remain required; no app or article changes in this maintenance commit.

## RC38 verified acceptance and comprehensive link audit
GitHub Actions run 45916714833 passed native Node regression, Python Bible parser fixtures, mobile Chromium smoke and offline reload, and actual RC37→RC38 upgrade with explicit activation, saved articles, notes and quiz preservation. Pages deployment 45916714653 passed. Official Bible build run 45913804782 (RC32) passed authentic archive fingerprint, 66 books, 1189 chapters, 31098 nonempty verses, 5 explicit empty references, offline Genesis/James/Revelation and local ZIP import. Link audit in RC38 checked 200/294 eligible URLs: 180 reachable, 20 unverified, 0 confirmed unavailable. To eliminate the 94 unchecked eligible URLs, the quality workflow now requests full coverage with --all; the default command remains a rotating 200-link sample for manual use. Added full-coverage fixture assertions. No app assets, content records or build version changed. The new full-audit CI run, device-specific Android acceptance, actual audio voice quality and independent editorial review remain outstanding.

## v2.0 RC39 — verified source-audit status
Actual RC38 quality workflow 45917486305 and Pages deployment 45917485813 both passed. The full link-audit job checked all 294 eligible URLs: 250 reachable, 44 unverified and zero HTTP 404/410. Updated the in-app Profile audit from the obsolete RC24 sample to the dated RC38 full inventory, with accessible progress, historical scope and an explicit distinction between unverified and broken. Existing alternate-source notices are retained as historical, not reclassified from aggregate data. RC39 source-level audit UI assertions and syntax checks passed; its own CI and deployment remain pending. All 204 articles are preserved. Individual unverified URLs have not been diagnosed in this round.

## RC39 source diagnostics maintenance
The latest confirmed comprehensive RC38 audit covered 294/294 eligible URLs: 250 reachable, 44 unverified, zero confirmed unavailable. Added a structured diagnostic report for every unresolved URL, including HTTP/transport/content-type classification, host aggregation, referenced roles, affected article IDs and a prioritized CSV/JSON report. Individual records are also printed as JSON lines in CI logs so the next editorial review can identify specific source issues without needing to download a ZIP artifact. No blocked or rate-limited requests are bypassed; existing reachability classification and per-host request limits remain intact. New fixture tests cover reason categories, affected-article deduplication and reachable exclusion. Application files and article content unchanged; RC39 retained. New native CI and individual diagnostics remain pending.

## v2.0 RC40 — targeted source alternatives and audit correction
RC39 diagnostic job 140241338524 checked 294 URLs: 250 reachable, 44 unverified, zero confirmed missing; 29 rate limited, 9 access restricted, 5 server errors, 1 audio content-type mismatch. 31 original article IDs were associated with unresolved URLs (including image credits/media, not just primary sources). Corrected the inventory's audio-extension heuristic for Wikisource File: landing pages, which are HTML rather than direct audio files. Updated primary reference notices using actual diagnostic roles; removed obsolete primary warnings for IDs 107,136,147 and 176, retained the recording alternate. Added relevant supplementary links for articles 75,99,137,143 from National Archives, USGS and NHCP retrieved public source results. They supplement rather than replace original evidence. Prior 204 content records preserved. Source-level assertions and syntax checks passed; RC40 native CI, actual link reachability and Android acceptance remain pending.

## v2.0 RC41 — practical judgment and family learning
RC40 quality jobs (run 45917989894) all passed. Added four original extended articles (205–208) on implementation intentions, Aristotelian equity, dialogic reading and the distinction between algorithms and heuristics. Source descriptions retrieved from NCI, MIT Classics, What Works Clearinghouse and OpenStax; original examples, limits, reflection and quiz included. Added a five-article practical-judgment path and extended the family path. Totals: 208 originals, 80 quizzes and 11 paths. Previous 204 records unchanged. Updated historical inventory expectations while keeping RC37 tests scoped to their original four articles. Syntax and source-level content assertions passed; RC41 native CI and device acceptance remain pending.

## v2.0 RC42 — dedicated extended reading collection
RC41 native quality workflow 45918212695 and Pages deployment 45918212508 passed. Added Deep reads as a dedicated collection of 8 original articles with at least 300 words, compact previews and visible word counts, reading-time total, topic and unread filtering, disabled/hidden exclusions, persistent selection and backup support. Switching from visual-only discovery resets to For you when entering this collection to avoid unintentionally excluding text-only essays. The existing full reader remains available with one tap. All 208 articles preserved. Added regression and Chromium assertions; source syntax and inventory checks passed, native RC42 acceptance remains pending.

## v2.0 RC43 — deepen existing readings
RC42 quality run 45923690125 and Pages deployment 45923689629 passed. Appended 1107 original words to eight existing articles (2,66,93,133,144,183,185,188), covering Stoic judgment, opportunity cost, family repair, compounding, emergency reserves, spaced practice, coping and courage. Preserved the existing text, article IDs, sources, quiz records and remaining 200 articles. Deep reads increased from 8 to 16; overall inventory stays at 208 articles and 80 quizzes. New material is editorial application and caveat, not an independent verification of the linked reference. Updated version and exact predecessor upgrade test. Content invariants and syntax passed; native RC43 CI and physical device acceptance remain pending.

## v2.0 RC44 — family, philosophy and biological timing
RC43 quality run 45923944420 and Pages deployment 45923943944 passed. Added 1159 original words to eight existing articles (15,103,134,156,157,181,186,189) on responsive parenting, sleep timing, boundaries, virtue, friendship, practical judgment, adjusting support and language. Preserved all prior text and identifiers, original references and quiz data. Deep reads increased to 24 of 208 originals; 80 quizzes and 11 paths retained. The new passages are explanatory applications, not independently verified findings; no medical treatment advice is introduced. Syntax and content invariants passed; native RC44 CI, deployment and physical device acceptance remain pending.

## v2.0 RC45 — practical character, cognition, financial literacy and fitness
RC44 quality run 45924171163 and Pages deployment 45924170540 passed. Appended 1589 original words to eleven existing articles (8,23,65,104,129,131,132,153,173,174,187). Added actionable examples, reasoning and qualifications without changing original text, references, IDs or quizzes. Deep reads increased from 24 to 35 of 208 originals; 80 quizzes and 11 paths remain. Examples are editorial interpretations rather than independently verified findings; financial and health examples are educational. Syntax and inventory invariants passed; native RC45 CI and deployment remain pending.
