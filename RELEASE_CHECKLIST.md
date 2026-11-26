# ARETÉ v2.0 RC4 acceptance checklist

This is a release candidate, not a claim of production readiness.

## Android / installed app
- [ ] Open app and verify version 2.0-rc4.
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
- [ ] Review remaining 166 articles, including source suitability and factual claims.
- [ ] Independently verify revised articles and actual media links.
