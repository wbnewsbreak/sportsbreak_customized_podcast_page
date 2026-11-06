#!/usr/bin/env python3
"""Generate and upload daily podcast clips for the priority leagues."""

import sys

from internetarchive.exceptions import (
    AccountAPIError,
    AuthenticationError,
    DirectoryTraversalError,
    InvalidChecksumError,
    ItemLocateError,
)
from pymongo.errors import PyMongoError
from requests.exceptions import RequestException

from generate import generate_audio_for_league
from upload import upload_mp3
from datetime import date

LEAGUES = ("nfl", "cfb", "nba", "mlb")


def main():
    """Generate and upload each league clip, reporting any failures."""
    failed = False
    for league in LEAGUES:
        print("Processing {}...".format(league.upper()), flush=True)
        try:
            audio = generate_audio_for_league(league)
            url = upload_mp3(audio, league)  # in case of needing to regenerate prev day, episode_date=date(2026, 10, 27))
        except (
            AccountAPIError,
            AuthenticationError,
            DirectoryTraversalError,
            InvalidChecksumError,
            ItemLocateError,
            OSError,
            PyMongoError,
            RequestException,
            RuntimeError,
            TypeError,
            ValueError,
        ) as error:
            print(
                "Error processing {}: {}".format(league.upper(), error),
                file=sys.stderr,
                flush=True,
            )
            failed = True
            continue

        print(url, flush=True)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
