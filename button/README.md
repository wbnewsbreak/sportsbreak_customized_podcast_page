# UI for podcast

This UI is designed to be in an iframe that will go in a wk web view in an ios app. It will be much smaller than a browser. The README.md stays human writen while AGENTS.md is the LLM optimized documentation. 

## Design
It should just be a button that says Play Your AI-generated Daily Briefing . On click, it should toggle between that and Pause. 

## Loading audio
https://archive.org/download/sportsbreak-{yyyy}-{mm}-{dd}/{league}.mp3 should be the source of the `<audio>` tag. The comma-separated `favorite_leagues` query parameter uses entries such as `league:nfl`; supported leagues (`nfl`, `mlb`, `cfb`, `nba`) play in the provided order. Unsupported entries are ignored, and if no supported league is provided, all four play in the default order. The `firebase_uid` query parameter is used for analytics attribution.

## Tracking
A big responsibility of this UI is to send heartbeat and other analytics messages to an analytics API that will store the usage data for later analysis that guides future improvements. 
- triggers when audio starts playing, every 15sec of audio, and when audio ends, and when page becomes visible
- sends user, league, %completion of audio file to api, sometimes sawPodcast event
