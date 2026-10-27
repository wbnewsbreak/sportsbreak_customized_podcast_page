"""Upload generated podcast MP3s to the Internet Archive."""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from internetarchive import upload

from config import EXEMPLAR_USERS

load_dotenv(Path(__file__).resolve().with_name(".env"))


def upload_mp3(
    audio: bytes | str | Path, league: str, episode_date: date | None = None
):
    """Upload an MP3 and return its Archive.org download URL.

    Archive.org item identifiers use the ``sportsbreak-YYYY-MM-DD`` format,
    and the uploaded filename is the league name (for example, ``nfl.mp3``).
    By default, the item date is tomorrow's UTC calendar date.
    """
    if league not in EXEMPLAR_USERS:
        raise ValueError(
            "Unsupported league {!r}; expected one of: {}.".format(
                league, ", ".join(sorted(EXEMPLAR_USERS))
            )
        )

    if isinstance(audio, bytes):
        audio_bytes = audio
    elif isinstance(audio, (str, Path)):
        audio_path = Path(audio).expanduser()
        if audio_path.suffix.lower() != ".mp3":
            raise ValueError("The audio file path must have an .mp3 extension.")
        audio_bytes = audio_path.read_bytes()
    else:
        raise TypeError("audio must be MP3 bytes or a path to an MP3 file.")

    if not audio_bytes:
        raise ValueError("Cannot upload an empty MP3.")
    if episode_date is not None and type(episode_date) is not date:
        raise TypeError("episode_date must be a datetime.date.")

    access_key = os.environ.get("ARCHIVE_ACCESS_KEY")
    secret_key = os.environ.get("ARCHIVE_SECRET_KEY")
    if not access_key or not secret_key:
        raise RuntimeError(
            "Set both ARCHIVE_ACCESS_KEY and ARCHIVE_SECRET_KEY in the "
            "environment or project .env file."
        )

    default_episode_date = datetime.now(timezone.utc).date() + timedelta(days=1)
    episode_date_id = (episode_date or default_episode_date).isoformat()
    identifier = "sportsbreak-{}".format(episode_date_id)
    filename = "{}.mp3".format(league)
    audio_file = BytesIO(audio_bytes)
    audio_file.name = filename

    metadata = {
        "title": "{} daily sports podcast ({})".format(
            league.upper(), episode_date_id
        ),
        "mediatype": "audio",
        "collection": "opensource_audio",
    }
    responses = upload(
        identifier,
        files=audio_file,
        metadata=metadata,
        access_key=access_key,
        secret_key=secret_key,
    )
    for response in responses:
        response.raise_for_status()

    return "https://archive.org/download/{}/{}".format(identifier, filename)