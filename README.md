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
