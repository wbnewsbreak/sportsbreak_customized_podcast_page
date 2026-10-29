#!/usr/bin/env python3
"""Fetch the latest news articles for a league's podcast episode."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError

from config import LEAGUES

load_dotenv(Path(__file__).resolve().with_name(".env"))

DATABASE_NAME = "sportsbreak"
MAX_ARTICLES = 3
THIRD_CATEGORY_PATH = "nb_meta.text_category_v3.third_cat"
SECOND_CATEGORY_PATH = "nb_meta.text_category_v3.second_cat"
LEAGUE_CATEGORY_FILTERS = {
    "nfl": {
        "{}.Sports_AmericanFootball_NFL".format(THIRD_CATEGORY_PATH): {
            "$exists": True
        }
    },
    "mlb": {
        "{}.Sports_Baseball_MLB".format(THIRD_CATEGORY_PATH): {"$exists": True}
    },
    "nba": {
        "{}.Sports_Basketball_NBA".format(THIRD_CATEGORY_PATH): {"$exists": True}
    },
    "cfb": {
        "{}.Sports_AmericanFootball".format(SECOND_CATEGORY_PATH): {"$exists": True},
        "{}.Sports_College".format(SECOND_CATEGORY_PATH): {"$exists": True},
    },
}


def load_mongo_url():
    """Return the configured MongoDB connection URL or raise if it is missing."""
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        raise RuntimeError("MONGO_URL is not set in the environment.")
    return mongo_url


def fetch_articles_for_league(mongo_url, league):
    """Return up to three recent league articles with their title and body text."""
    if league not in LEAGUES:
        raise RuntimeError(
            "Unsupported league {!r}. Choose one of: {}.".format(
                league, ", ".join(sorted(LEAGUES))
            )
        )

    articles = []
    with MongoClient(mongo_url) as client:
        collection = client[DATABASE_NAME].nb_news
        cursor = collection.find(
            LEAGUE_CATEGORY_FILTERS[league],
            {"_id": 0, "title": 1, "body": 1},
        ).sort("published_at", DESCENDING).limit(MAX_ARTICLES)

        for document in cursor:
            title = document.get("title")
            body = document.get("body")
            if (
                not isinstance(title, str)
                or not title.strip()
                or not isinstance(body, str)
                or not body.strip()
            ):
                continue

            title = title.strip()
            articles.append(
                {
                    "title": title,
                    "text": "{}\n\n{}".format(title, body.strip()),
                }
            )
    if not articles:
        raise RuntimeError(
            "No usable {!r} articles found in the nb_news collection.".format(league)
        )
    return articles


def main():
    """Print today's NFL article content; return a process exit status."""
    try:
        articles = fetch_articles_for_league(load_mongo_url(), "nfl")
        for article in articles:
            print("--- {} ---".format(article["title"]))
            print(article["text"])
    except RuntimeError as error:
        print("Error: {}".format(error), file=sys.stderr)
        return 1
    except PyMongoError as error:
        print("Error: MongoDB lookup failed: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
