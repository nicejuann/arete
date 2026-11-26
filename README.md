# ARETÉ v0.2 — Personal prototype

A dependency-free, mobile-first Progressive Web App. No account, API keys, build step, analytics, ads or paid services. This is a first version, not a public-ready product.

## Deploy for free
1. Sign in to GitHub and create a **public** repository named `arete` (the code and starter content will be public; personal notes are stored on your device, not in the repository). Do not upload personal exports.
2. Extract this archive. Upload the files at its root to the repository root, including manifest, icons and service worker. Commit.
3. In repository Settings → Pages, choose Deploy from a branch, select `main` and `/ (root)`, and save. Open the published HTTPS URL shown there once available. Free hosting eligibility and policies can change.
4. On Android Chrome, visit that URL, then use the menu → Install app or Add to Home screen (wording varies). Open the app once while online to allow offline caching.
5. Enable Faith in Profile if desired. Use the browser's device-level speech service for narration, subject to device availability and voice settings.

## Local development
Run `python -m http.server 8000` in the extracted folder, then open `http://localhost:8000`. No dependencies. The separate standalone preview HTML is for trying the interface without deploying; it cannot be installed as a PWA and local file storage support varies.

## Implemented
- 50 original introductory insights in 11 categories, with reference links, optional Christian reflections, deeper explanations and reflection prompts.
- Five-card vertical feed with deliberate continuation; adaptive category weighting and novelty/diversity rules, search, bookmarks, notes, read flags, local preferences, data export/import, dark/light appearance.
- Original category artwork; device narration; links to free books and external video collections.
- Manifest, icons and offline cache implementation. No external requests during ordinary reading except user-selected source links or device speech behavior.

## Deferred
Automated content acquisition, content editor and verification pipeline; in-feed video; PDF/EPUB import and integrated Bible reader; actual social media app interception; cloud sync; production accessibility, security, licensing and behavioral review. External websites may have ads, data collection or access restrictions. Device speech may require an internet connection depending on the voice.

## Editorial status
Starter cards are original short explanations and reflections with links to supporting resources, not copied publications. References were selected using source research; a separate exhaustive claim-by-claim editorial and licensing audit has not been performed. Before public release, verify every card, source and license independently. The Christianity category is disabled by default and can be enabled without an account. No user-specific identity or private data is included.

## Testing status
JavaScript syntax checks passed for app, content and service worker. Chromium mobile-size rendering and core interactions (feed, expanding cards, bookmarks, notes, mark read, topic switch, search) passed in an inline test harness using simulated storage. Direct local HTTP and file navigation were blocked by the test environment, so native storage persistence, service-worker offline behavior, actual Android installation, narration and device sharing remain unverified. Test these on the published HTTPS site before calling the PWA deployment complete.

## v0.2 changes
All 50 starter articles expanded with original examples; full content visible directly in feed. Existing IDs and local storage schema retained. Improved typography, concept panels, four original educational diagrams, selected links to human narration and educational videos, and device voice selection. Media requires internet. This remains a prototype; a comprehensive factual/licensing audit, photographic library, automated content ingestion, native audio quality and Android regression testing remain pending. The original testing status below applies only to v0.1.

## v0.2.1 update delivery
Visible version label, versioned static assets, navigation network-first with offline fallback, service-worker update checks on foreground. No storage schema changes. Android update and deployment verification pending.

## v0.3
60 stable-ID articles including ten new discoveries, credited remote images, one in-feed NASA video, three interactive quizzes and an optional publisher headline digest. Remote media requires internet and may fail to load; credit and source links remain. Fresh headlines are publisher links, not editorially approved new articles. No paid APIs, trackers or autoplay. Existing local data retained. Android and remote asset rendering require retesting.

## v0.3.1 — fresh-content automation
A scheduled GitHub Actions workflow retrieves NASA and Library of Congress RSS headlines daily, using only standard free public-repository runners and Python's standard library. Run it manually from Actions → Refresh educational headlines → Run workflow to initialize it. The app reads the public raw GitHub digest because commits made with GITHUB_TOKEN do not necessarily trigger a branch-based Pages rebuild. Source failures keep previous entries; no article body is copied. Scheduled runs, runner policies and source availability are not guaranteed. Remote fetches contact GitHub/NASA/museum servers; no private bookmarks are transmitted.

## v0.4 — Reading and discovery
80 curated articles (20 added, IDs 61–80), including four new quizzes, two additional attributed photo assignments, new discovery modes and local TXT reading shelf. Two complete Psalms (WEB Classic, public domain) included as a Scripture starter, not a complete Bible. The personal shelf and reading positions use localStorage separately from existing bookmark data; the old export does not include imported books. PDF/EPUB support, full Scripture reader, image delivery verification and comprehensive editorial audit remain pending. RSS workflow expanded to five source feeds; availability and first successful run still require verification. No paid service added.

## v0.5 — broader discoveries and chapter reader
100 original curated articles; 20 new posts, 5 new quizzes. Four dated publisher links seeded manually (distinct from automatic refresh). On-demand WEB Bible chapter navigation for 66 books using bible-api.com, with per-chapter offline cache where device storage permits; no bulk download. API availability and Android playback/reading must be tested. Existing local data retained; imported books and cached Bible chapters are not included in the existing bookmarks export. The 300-post target, complete offline Bible, PDF/EPUB parsing, remote media checks and comprehensive editorial audit remain pending. No paid services introduced.

## v0.6 — discovery and backup
112 curated articles with 12 new discoveries and four new quizzes. Added Rizal's two novels as links to free historical translations; added headline expansion controls, reading shelf backup and restore, NASA Image of the Day source, direct Smithsonian feed endpoints and a push trigger for the RSS workflow. No paid service introduced. Automatic refresh execution, source availability, Android storage restore, and media playback remain to be verified. Cached Bible chapters are excluded from backups. Backups may contain private notes and imported books; do not publish them. Full PDF/EPUB and 300 articles remain pending.

## v0.7 — visual stories and balanced publisher digest
118 original curated posts, six new art stories with CC0 image and credit records verified in The Metropolitan Museum of Art's collection API, 15 image-led posts and 17 quizzes. Automated headline commit verified before this release: 42 items on 2026-11-26 UTC. New digest balances topics, filters administrative announcements by default, preserves All headlines, and updates without rerendering the reader. Offline fallback for headline data; remote source articles and photographs still need internet. Android rendering and comprehensive editorial verification remain pending. No paid services added.

## v0.8 — substantive open reading
Daily curated-topic Wikipedia lead-excerpt collection via standard-library Python and GitHub Actions. Up to 16 topics per run, 100–550 words and 2600 characters maximum per accepted excerpt, archive up to 100. Site CC BY-SA 4.0 license check, stable page IDs, source/history/revision/license links and plain-text excerpt notice. No images imported from Wikipedia, no AI summaries, no paywalled article copying. Automatically imported material is explicitly not editorially reviewed; source pages can contain additional attribution notices. New Beyond the headline feed, topic filtering, offline text cache, separate saved excerpts and backup support. Original article count remains 118. First automated open-reading run and actual Android testing pending; API can fail or rate-limit. Existing headline feed verified separately. No paid services added.

## v0.9 — visual discovery and human narration
Prior automated text import verified: 11 open-license excerpts and 42 headlines. Added a third workflow for up to six public-domain Met artwork records per day, 120-record cap, with CC0 metadata and credit. Images are streamed from the museum. Five LibriVox catalog links, one on-demand audio player sourced from the catalog, four NASA video links, and an Astronomy 2e textbook link. No autoplay or paid services. Audio playback, Android image rendering and first gallery run still need verification. Original article count unchanged.

## v1.0 RC1 — release candidate
Focused collection navigation, unread-only toggle, unified search across four collections with compact results and full article/excerpt reading, larger text option, and editorial typography. Automated Node regression checks and a weekly/push link audit report unreachable and unverified sources separately without deleting links. Link audit output is an Actions artifact. Existing article IDs and local data keys preserved. Gallery first import remains pending as of preparation; live Android/PWA, media and full source audit remain unverified. Release candidate, not production completion. No paid services added.
