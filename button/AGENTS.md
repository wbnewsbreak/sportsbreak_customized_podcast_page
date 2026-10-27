# Button Directory Guide

## Purpose and Runtime

This directory contains a small HTML/CSS/JavaScript audio player designed for
embedding in a WKWebView iframe in an iOS app. Keep the interface compact: a
single Play button that changes to Pause during playback, with a small status
area for errors.

Open `index.html` directly for local testing. The league mapping is a local
script, not a network request, so the page can read it without fetching a JSON
file. In `index.html`, load `sportsbreak_users.js` before `app.js`; the mapping
script assigns `window.FIREBASE_UID_TO_LEAGUES`.

## User and League Selection

- Read the user's Firebase UID from the `firebase_uid` query parameter.
- Use that UID to select the league array from
  `window.FIREBASE_UID_TO_LEAGUES`.
- If the UID is missing, unmapped, or its mapping is invalid, use the fallback
  leagues in this order: `nfl`, `mlb`, `cfb`, `nba`.
- Do not duplicate or hardcode the full user mapping in `app.js`.
- The retained `convert_users.py` utility converts an array of
  `{ "firebase_uid": "...", "leagues": [...] }` records into a UID-keyed JSON
  object in `sportsbreak_users.json`. It does not generate the JavaScript
  wrapper; if refreshing the browser mapping, ensure the resulting
  `sportsbreak_users.js` assigns the object to
  `window.FIREBASE_UID_TO_LEAGUES`.

## Audio Playback

- Build each audio URL as
  `https://archive.org/download/sportsbreak-YYYY-MM-DD/<league>.mp3`.
- Use the current UTC calendar date for the episode ID. The upload pipeline
  defaults to tomorrow's UTC calendar date so that it is available as that
  date begins; keep these date rules aligned.
- Play each selected league in order, one after another. Preserve pause/resume,
  restart-after-completion, and visible playback/load errors.
- Keep the page usable in a narrow embedded web view.

## Analytics

- Send analytics to the configured Apps Script URL through the shared POST
  helper in `app.js`.
- Apps Script may redirect. Use the existing `no-cors` request with a
  CORS-simple `text/plain` content type and JSON-stringified request body;
  responses are opaque, so do not depend on reading their status or body.
- On playback start, every 15 seconds of audio, and playback end, send the user,
  current league, and completion percentage. The current payload field is
  `completionPercent`; keep it aligned with the deployed analytics handler.
- On initial load when visible and whenever the document becomes visible,
  send an impression payload with `league: "sawPodcast"` and no completion
  percentage.
- Report request failures to the console and do not interrupt playback.

## Files and Validation

- `index.html`: player markup and ordered script/style includes.
- `styles.css`: compact, responsive player styling.
- `app.js`: date selection, league playlist, playback controls, and analytics.
- `sportsbreak_users.js`: local UID-to-leagues mapping consumed by `app.js`.
- `convert_users.py`: reusable input-array-to-JSON-object conversion utility.

After changing JavaScript, run `node --check button/app.js` from the project
root. After changing the conversion utility, run
`python3 -m py_compile button/convert_users.py`. Prefer offline tests with
mocked audio and analytics; do not make real Archive.org or analytics requests
as part of routine validation.
