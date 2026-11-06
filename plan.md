# Human edited plan that should be reflected in Jira can be commited to github by agents

## Done: 
- pipeline to read mongodb, make podcast, publish podcast
- frontend to embed that plays podcast and records analytics
- analytics spreadsheet builder
- more work on making the button render nicely
- dynamically fetch leagues followed from mongodb instead of relying on snapshot, requires changing url parameters and editing the iframe building logic in the app

## In Progress:
- measure usage

## Potential future work, gated by podcast success (50% of podcast listeners listen to it at least twice)
- deploy to cloud cron job
- expand beyond nfl cfb mlb nba
- store listened state of podcast to show things like (resume, finished)

## Jira task: https://particlemedia.atlassian.net/browse/SPR-260