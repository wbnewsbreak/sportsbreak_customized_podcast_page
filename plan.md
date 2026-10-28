# Human edited plan that should be reflected in Jira

## Done: 
- pipeline to read mongodb, make podcast, publish podcast
- frontend to embed that plays podcast and records analytics
- analytics spreadsheet builder

## In Progress:
- more work on making the button render nicely
- research redoing the mongodb pipeline to not rely on curator_items
- dynamically fetch leagues followed from mongodb instead of relying on snapshot, requires changing url parameters and editing the iframe building logic in the app

## Potential future work, gated by podcast success (50% of podcast listeners listen to it at least twice)
- deploy to cloud cron job
- expand beyond nfl cfb mlb nba

## Jira task: https://particlemedia.atlassian.net/browse/SPR-260