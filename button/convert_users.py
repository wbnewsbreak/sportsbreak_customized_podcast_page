import json
import os
from pathlib import Path


path = Path(__file__).with_name("sportsbreak_users.json")
records = json.loads(path.read_text(encoding="utf-8"))
if not isinstance(records, list):
    raise TypeError("Expected sportsbreak_users.json to contain an array.")

users = {}
for index, record in enumerate(records):
    if (
        not isinstance(record, dict)
        or not isinstance(record.get("firebase_uid"), str)
        or not isinstance(record.get("leagues"), list)
    ):
        raise ValueError(f"Invalid user record at index {index}.")

    uid = record["firebase_uid"]
    if uid in users:
        raise ValueError(f"Duplicate firebase_uid at index {index}: {uid!r}")
    users[uid] = record["leagues"]

temporary_path = path.with_suffix(path.suffix + ".tmp")
try:
    with temporary_path.open("w", encoding="utf-8") as output:
        json.dump(users, output, ensure_ascii=False, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    temporary_path.chmod(path.stat().st_mode & 0o777)
    temporary_path.replace(path)
except Exception:
    temporary_path.unlink(missing_ok=True)
    raise

converted = json.loads(path.read_text(encoding="utf-8"))
if len(converted) != len(records) or any(
    converted[record["firebase_uid"]] != record["leagues"] for record in records
):
    raise RuntimeError("Post-write verification failed.")

print(f"Converted and verified {len(converted)} user records.")
