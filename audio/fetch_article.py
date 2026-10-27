#!/usr/bin/env python3
"""Fetch recommended articles for a league's podcast episode."""

import os
import sys
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import CURATORS, EXEMPLAR_USERS

load_dotenv(Path(__file__).resolve().with_name(".env"))

DATABASE_NAME = "sportsbreak"
REQUEST_TIMEOUT_SECONDS = 20
MAX_ARTICLES = 3


class ArticleTextParser(HTMLParser):
    """Collect readable text while skipping common non-content HTML elements."""

    EXCLUDED_TAGS = {
        "aside",
        "footer",
        "form",
        "head",
        "header",
        "nav",
        "noscript",
        "script",
        "style",
        "svg",
    }
    BLOCK_TAGS = {
        "address",
        "article",
        "blockquote",
        "br",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "li",
        "main",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }

    def __init__(self):
        """Initialize parser state for excluded elements and collected text."""
        super().__init__(convert_charrefs=True)
        self._excluded_tags = []
        self._text_parts = []

    def handle_starttag(self, tag, _attrs):
        """Track excluded elements and separate text at block boundaries."""
        tag = tag.lower()
        if tag in self.EXCLUDED_TAGS:
            self._excluded_tags.append(tag)
            return
        if self._excluded_tags:
            return
        if tag in self.BLOCK_TAGS:
            self._text_parts.append("\n")

    def handle_data(self, data):
        """Collect text outside excluded elements."""
        if self._excluded_tags:
            return
        self._text_parts.append(data)

    def handle_endtag(self, tag):
        """Stop excluding a closed element and separate block-level text."""
        tag = tag.lower()
        if tag in self._excluded_tags:
            index = len(self._excluded_tags) - 1 - self._excluded_tags[::-1].index(tag)
            del self._excluded_tags[index:]
            return
        if self._excluded_tags:
            return
        if tag in self.BLOCK_TAGS:
            self._text_parts.append("\n")

    def article_text(self):
        """Return normalized page text, with nonempty lines separated by newlines."""
        lines = [
            " ".join(line.split())
            for line in "".join(self._text_parts).splitlines()
        ]
        return "\n".join(line for line in lines if line)


def load_mongo_url():
    """Return the configured MongoDB connection URL or raise if it is missing."""
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        raise RuntimeError("MONGO_URL is not set in the environment.")
    return mongo_url


def is_non_article_url(url):
    """Return whether a URL points to X or YouTube rather than an article."""
    try:
        hostname = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return True
    return any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in ("x.com", "youtube.com")
    )


def article_candidates_for_league(mongo_url, league):
    """Return digest articles with a matching league curator.

    Each result is a dictionary with ``title``, ``url``, and ``description``
    keys. The description may be ``None`` when the curator item has no
    description. Raises RuntimeError when the league or today's digest has no
    matching candidate articles.
    """
    if league not in EXEMPLAR_USERS:
        raise RuntimeError(
            "Unsupported league {!r}. Choose one of: {}.".format(
                league, ", ".join(sorted(EXEMPLAR_USERS))
            )
        )

    today = date.today().isoformat()
    with MongoClient(mongo_url) as client:
        database = client[DATABASE_NAME]
        digest = database.catch_me_up_digests.find_one(
            {"firebase_uid": EXEMPLAR_USERS[league], "day": today}
        )
        if digest is None:
            raise RuntimeError(
                "No catch-me-up digest found for league {!r} on {}.".format(
                    league, today
                )
            )

        articles = digest.get("articles") or []
        if not isinstance(articles, list) or not articles:
            raise RuntimeError(
                "Digest for league {!r} on {} has no articles.".format(league, today)
            )

        article_metadata = []
        seen_urls = set()
        for article in articles:
            if not isinstance(article, dict):
                continue
            title = article.get("title")
            url = article.get("url")
            if (
                not isinstance(title, str)
                or not isinstance(url, str)
                or not url
                or is_non_article_url(url)
                or url in seen_urls
            ):
                continue
            seen_urls.add(url)
            article_metadata.append({"title": title, "url": url})

        if not article_metadata:
            raise RuntimeError(
                "Digest for league {!r} on {} has no article URLs.".format(
                    league, today
                )
            )

        urls = [article["url"] for article in article_metadata]
        curator_items_by_url = {}
        for item in database.curator_items.find(
            {"external_url": {"$in": urls}},
            {"external_url": 1, "curator_id": 1, "description": 1},
        ):
            url = item.get("external_url")
            if url and CURATORS.get(item.get("curator_id")) == league:
                curator_items_by_url[url] = item

    candidates = [
        {
            **article,
            "description": curator_items_by_url[article["url"]].get("description"),
        }
        for article in article_metadata
        if article["url"] in curator_items_by_url
    ]
    if not candidates:
        raise RuntimeError(
            "No digest articles are associated with a {!r} curator.".format(league)
        )
    return candidates


def fetch_article_text(url):
    """Fetch a page and return normalized readable text parsed from its HTML."""
    if not url.startswith(("http://", "https://")):
        raise RuntimeError("Unsupported article URL: {!r}".format(url))

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; podcast-prototype/1.0)"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=REQUEST_TIMEOUT_SECONDS
        ) as response:
            html = response.read().decode(
                response.headers.get_content_charset() or "utf-8",
                errors="replace",
            )
    except urllib.error.HTTPError as error:
        raise RuntimeError(
            "Article request failed with HTTP {} for {}.".format(error.code, url)
        ) from error
    except urllib.error.URLError as error:
        raise RuntimeError(
            "Could not retrieve article at {}: {}".format(url, error.reason)
        ) from error

    parser = ArticleTextParser()
    parser.feed(html)
    article_text = parser.article_text()
    if article_text:
        return article_text
    raise RuntimeError(
        "No readable article text found on the source page at {}.".format(url)
    )


def fetch_articles_for_league(mongo_url, league):
    """Return up to MAX_ARTICLES article dictionaries for a league.

    Each dictionary contains ``title``, ``url``, ``text``, and ``description``.
    Page text is used when available; otherwise ``text`` falls back to the
    curator description. Raises RuntimeError if no usable content is found.
    """
    candidates = article_candidates_for_league(mongo_url, league)
    articles = []
    retrieval_errors = []
    for candidate in candidates:
        article_text = None
        try:
            article_text = fetch_article_text(candidate["url"])
        except (OSError, RuntimeError, ValueError) as error:
            retrieval_errors.append("{}: {}".format(candidate["url"], error))

        if not article_text:
            description = candidate.get("description")
            if isinstance(description, str) and description.strip():
                article_text = description.strip()
            else:
                if not retrieval_errors or not retrieval_errors[-1].startswith(
                    candidate["url"] + ":"
                ):
                    retrieval_errors.append(
                        "{}: no article text or curator description available".format(
                            candidate["url"]
                        )
                    )
                continue

        articles.append(
            {
                "title": candidate["title"],
                "url": candidate["url"],
                "text": article_text,
                "description": candidate.get("description") or "",
            }
        )
        if len(articles) == MAX_ARTICLES:
            break

    if not articles:
        detail = " {}".format(retrieval_errors[-1]) if retrieval_errors else ""
        raise RuntimeError(
            "No article content could be fetched or found in descriptions for "
            "{} {!r} curator articles.{}".format(
                len(candidates), league, detail
            )
        )
    return articles


def main():
    """Print today's NFL article content; return a process exit status."""
    try:
        articles = fetch_articles_for_league(load_mongo_url(), "nfl")
        for article in articles:
            print("--- {} ({}) ---".format(article["title"], article["url"]))
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
