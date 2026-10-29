# Project Guide

## Instructions for Coding Agents

- Do not edit `README.md`. It contains human-readable project notes provided
  as context; keep agent-specific instructions and project context in this
  `AGENTS.md` file instead.
- Put documentation intended for future coding agents in `AGENTS.md`, not
  `README.md`.

## System Overview

This project creates a spoken sports-news podcast for one league. The flow is:

1. `config.py` lists the leagues supported by the generator. League-to-content
   filtering is defined in `fetch_article.py`.
2. `fetch_article.py` queries the `sportsbreak` MongoDB database's `nb_news`
   collection for the selected league, sorts by `published_at` descending, and
   takes up to three articles. NFL, MLB, and NBA use their specific
   `nb_meta.text_category_v3.third_cat` category; CFB requires both
   `Sports_AmericanFootball` and `Sports_College`.
3. Each selected article's `title` and `body` are combined into the text passed
   to generation. No webpage fetch, digest lookup, or `curator_items` lookup is
   part of this flow.
4. `generate.py` sends the article title and body text to
   the text-generation API to produce a short spoken script, then sends that
   script to text-to-speech and returns MP3 bytes (or writes them to a file
   when run directly).
5. `upload.py` accepts MP3 bytes or a file path and uploads it to Archive.org
   under an item identifier formatted as `sportsbreak-YYYY-MM-DD`, with the
   file named `<league>.mp3`, and adds it to the `opensource_audio` community
   collection.
   Its `upload_mp3(audio, league, episode_date=None)` function returns the
   Archive.org download URL; the date defaults to today. Archive.org processes
   uploads asynchronously, so a successful upload response may precede public
   availability of the item and download URL. The prefixed date identifier
   intentionally groups that day's distinct league files in one item.
6. `main.py` runs generation and upload for `nfl`, `cfb`, `nba`, and `mlb`,
   printing each Archive.org download URL without saving intermediate MP3s.

## Product Context and Current Constraints

- The long-term goal is a personalized daily briefing assembled from the
  leagues each user follows. The current approach generates reusable league
  clips rather than a separate clip for every user.
- Keep generation limited to the current priority leagues: `nfl`, `mlb`, `nba`,
  and `cfb`. The CFB cutoff reflects the current prioritization; clips are
  intended to be stitched together for users based on their followed leagues.
- The finished episode should include an AI-generated-content disclaimer.
- `archive.org` is the current low-cost, fast-to-launch audio host, not a
  long-term storage requirement.
- The pipeline is currently run locally each day. Do not add a scheduled job
  or change the execution environment without addressing the required MongoDB
  access through the developer VPN.

## Important Data and Content Details

- `nb_news` documents are selected by `published_at` and
  `nb_meta.text_category_v3.third_cat`; their `title` and `body` fields provide
  the text passed to the transcript generator.
- The transcript prompt treats source text as untrusted content rather than
  instructions.
- Keep the three-article limit. Report when no usable article content is found;
  do not silently produce an empty episode.

## Modules

- `config.py`: names of the leagues supported by the generator.
- `fetch_article.py`: MongoDB lookup and league filtering. Its
  `fetch_articles_for_league()` results contain `title` and `text`, where
  `text` combines the article title and body.
- `generate.py`: command-line orchestration, transcript generation, TTS, and
  MP3 output. `generate_audio_for_league()` returns MP3 bytes for orchestration;
  `--league` accepts the leagues configured in `config.py` and defaults to
  `nfl`.
- `main.py`: generates and uploads clips for all current priority leagues.
- `upload.py`: `upload_mp3()` sends MP3 bytes or a local MP3 path to Archive.org.

## Running and Validation

- Install Python dependencies from `requirements.txt`.
- Set `MONGO_URL`, `OPENAI_API_KEY`, `OPENAI_API_BASE`, and
  `PODCAST_OPENAI_API_KEY` in the environment or local `.env` file. For
  Archive.org uploads, set `ARCHIVE_ACCESS_KEY` and `ARCHIVE_SECRET_KEY` in
  `.env`; obtain these S3-like API keys from
  https://archive.org/account/s3.php. Never expose or commit credentials.
- Keep `.env` private and out of version control.
- Generate an episode with `python3 generate.py --league nba`; use `--output`
  to select an MP3 destination. `python3 fetch_article.py` prints the default
  NFL article content for troubleshooting.
- Run the full daily generation and upload pipeline with `python3 main.py`.
- There is no configured test suite in this repository. For focused changes,
  use `python3 -m py_compile fetch_article.py generate.py main.py upload.py` and
  add/run offline checks for changed parsing or prompt behavior. Avoid live
  database or API calls in routine validation.
