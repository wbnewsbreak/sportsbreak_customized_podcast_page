# these users only follow these leagues, so use their recommended articles
EXEMPLAR_USERS = {
    "nfl": "rp9EUeclybVKz2V3PDkbCFT64Dr1",
    "nba": "SyazWKc9DbPj9DlP0dxSiFwqnUU2",
    "mlb": "rRx3VrVJdtXQkvfZTRsmbWZM7j42",
    "cfb": "BwP6RLnxa5Xe2rLmegXTdFZIOvC2"
}
# search the collection catch_me_up_digests for firebase_uid matching the appropriate one and day = "yyyy-mm-dd" of today
# go to .articles of that document, error loudly if there is no document matching those
# Each element of .articles has a .title and .url
# skip and go to next one if .url has x.com or youtube.com in it because that isn't an article 
# for each of them, search the .url in the collection curator_items matching on .external_url
# that document from curator_items will have a .curator_id

CURATORS = {
    "81cegp18": "nba",
    "y7lq7qgw": "nfl",
    "b9fdo2ib": "mlb",
    "8zwgps1g": "cfb"
}

# ensure that the curator matches the requested league
# using external_url get the article text, fall back to .description on any issues
# the top 3 of the league go into the llm prompt for summarization and transcriptification and then tts