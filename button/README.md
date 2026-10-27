# UI for podcast

This UI is designed to be in an iframe that will go in a wk web view in an ios app. The WK web view will be very small, see the "Play" button in reference.png

## Design
It should just be a button that says Play Your AI-generated Daily Briefing . On click, it should toggle between that and Pause. 

## Loading audio
https://archive.org/dowload/sportsbreak-{yyyy}-{mm}-{dd}/{league}.mp3 should be the source of the `<audio>` tag. Based on the url's firebase_uid query parameter, it will populate the correct leagues in to go through, one after another. 

## Tracking
A big responsibility of this UI is to send heartbeat and other analytics messages to an analytics API that will store the usage data for later analysis that guides future improvements. 
- triggers when audio starts playing, every 15sec of audio, and when audio ends, and when page becomes visible
- sends user, league, %completion of audio file to api, sometimes sawPodcast event

