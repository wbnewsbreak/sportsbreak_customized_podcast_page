# Customized Podcast for SportsBreak users

This generates a podcast out of the top stories for a specific league. The long term vision is a customized daily briefing podcast for each user.

## Architecture
fetch_article.py reads mongodb for the right league and gets top articles. It reads from config.py which has more documentation on this. 
- probably just need to search for .nb_meta.text_category_v3.third_cat having the attribute of Sports_AmericanFootball_NFL, Sports_Baseball_MLB, Sports_Basketball_NBA or .nb_meta.text_category_v3.third_cat having only attributes of Sports_AmericanFootball and Sports_College. 
    - without any importance score, use jsut 3 most recent as seen in published_at attribute
    - title and body attributes provide all text needed, no need to search the actual webpage
    - use the nb_news collection
    - {'nb_meta.text_category_v3.third_cat.Sports_AmericanFootball_NFL':{$exists:true}}
generate.py handles turning article text and description into a podcast audio clip. 
upload.py handles uploading the clips to archive.org with the right format for later loading in the html page frontend, uses tomorrow's date so that episodes that are played tomorrow will work correctly
main.py strings them all together

## Testing scopes
We don't know yet if this is actually a useful idea. To not put too much engineering effort before then, we're only generating podcast clips for the biggest leagues sportsbreak users favorite: nfl, mlb, nba, cfb. After CFB there is an elbow point. These league clips will be stitched together for users based on their followed leagues. There will be an ending "ai generated" disclaimer. 

Want to have league clips shared across users for now to avoid massive generation times. 

archive.org is used instead of s3 buckets or whatever because it is free to get this up fast. Archive has a few minute availability waiting time after upload

I'll run the pipeline every day locally because it isn't worth it yet to set up an actual cron job and get mongodb access with developer vpn somehow on that cluster. 

## Potential future work:
1. Start each clip with "In the {league}, the latest news..." or something similar