# Button Directory Guide

## Purpose and Runtime

This directory contains a small HTML/CSS/JavaScript audio player designed for
embedding in a WKWebView iframe in an iOS app. Keep the interface compact: a
single Play button that changes to Pause during playback, with a small status
area for errors.

Open `index.html` directly for local testing. The player reads the favorite
leagues directly from its URL query parameters.

## User and League Selection

- Read the user's Firebase UID from the `firebase_uid` query parameter for
  analytics attribution.
- Read favorite leagues from the comma-separated `favorite_leagues` query
  parameter, whose entries use the `league:<code>` format.
- Play only supported league codes (`nfl`, `mlb`, `cfb`, and `nba`), ignoring
  other entries. If none are supported or the parameter is absent, play all
  four in the default order: `nfl`, `mlb`, `cfb`, `nba`.
- Do not use the UID-to-leagues mapping in `sportsbreak_users.js` to choose
  clips.

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

- `index.html`: player markup and script/style includes.
- `styles.css`: compact, responsive player styling.
- `app.js`: date selection, league playlist, playback controls, and analytics.

After changing JavaScript, run `node --check button/app.js` from the project
root. After changing the conversion utility, run
`python3 -m py_compile button/convert_users.py`. Prefer offline tests with
mocked audio and analytics; do not make real Archive.org or analytics requests
as part of routine validation.
