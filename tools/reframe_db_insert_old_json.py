#!/usr/bin/env python3
"""
Import ReFrame JSON session files into a SQLite sessions table.

Behavior:
- Prefer session_info.uuid if present.
- Otherwise search recursively for a "uuid" key anywhere in the JSON.
- If no UUID found, generate a uuid4 and add it into the session_info in-memory.
- Extract session start/end timestamps from session_info.time_start_unix / time_end_unix,
  or parse time_start/time_end in the "YYYYMMDDTHHMMSS+ZZZZ" format as a fallback.
- Insert into sessions(uuid, session_start_unix, session_end_unix, json_blob, report_file)
  only if uuid is not already present in the DB.

Adjust JSON_DIR and DB_PATH variables as needed.
"""
import os
import json
import sqlite3
import uuid
import time
from datetime import datetime

# ========== CONFIGURE THESE ==============
JSON_DIR = "/path/to/reframe/json/files"
DB_PATH = "/path/to/results.db"
# ==========================================

def find_uuid_in_session(data):
    """Return uuid (string) found under session_info.uuid, or None."""
    if not isinstance(data, dict):
        return None
    si = data.get("session_info")
    if isinstance(si, dict):
        val = si.get("uuid") or si.get("UUID")
        if isinstance(val, str):
            return val
    return None

def find_uuid_recursive(obj):
    """Recursively search for the first key named 'uuid' (case-insensitive) and return its string value."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == "uuid" and isinstance(v, str):
                return v
        for v in obj.values():
            found = find_uuid_recursive(v)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_uuid_recursive(item)
            if found:
                return found
    return None

def validate_uuid_str(u):
    """Return canonical uuid string if valid, else raise ValueError."""
    try:
        uu = uuid.UUID(u)
        return str(uu)
    except Exception as e:
        raise ValueError(f"Invalid UUID: {u}") from e

def parse_time_value(val):
    """Try to produce a unix timestamp (float) from a few possible formats."""
    if val is None:
        return None
    # If already numeric:
    if isinstance(val, (int, float)):
        return float(val)
    # If string numeric:
    try:
        return float(val)
    except Exception:
        pass
    # Try ReFrame basic ISO-like: YYYYMMDDTHHMMSS+ZZZZ (example: 20250803T151940+0300)
    if isinstance(val, str):
        try:
            dt = datetime.strptime(val, "%Y%m%dT%H%M%S%z")
            return dt.timestamp()
        except Exception:
            pass
        # try ISO 8601 parse (Python 3.7+)
        try:
            dt = datetime.fromisoformat(val)
            return dt.timestamp()
        except Exception:
            pass
    return None

def ensure_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions(
      uuid TEXT PRIMARY KEY,
      session_start_unix REAL,
      session_end_unix REAL,
      json_blob TEXT,
      report_file TEXT
    )
    ''')

def import_json_sessions(json_dir, db_path, generate_deterministic=False):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # ensure_table(cur)
    conn.commit()

    cur.execute("SELECT uuid FROM sessions")
    existing_uuids = set(row[0] for row in cur.fetchall())

    stats = {
        "found_files": 0,
        "inserted": 0,
        "skipped_already_in_db": 0,
        "malformed_json": 0,
        "generated_uuid": 0,
        "invalid_uuid_fixed": 0,
    }

    for root, _, files in os.walk(json_dir):
        for fname in files:
            if not fname.lower().endswith(".json"):
                continue
            stats["found_files"] += 1
            fullpath = os.path.join(root, fname)
            try:
                with open(fullpath, "r", encoding="utf-8") as fh:
                    raw = fh.read()
                    data = json.loads(raw)
            except Exception as e:
                print(f"[ERROR] Could not parse JSON {fullpath}: {e}")
                stats["malformed_json"] += 1
                continue

            u = find_uuid_in_session(data)
            if not u:
                u = find_uuid_recursive(data)

            generated = False
            invalid_fixed = False
            if not u:
                if generate_deterministic:
                    u = str(uuid.uuid5(uuid.NAMESPACE_URL, raw))
                else:
                    u = str(uuid.uuid4())
                if "session_info" not in data or not isinstance(data.get("session_info"), dict):
                    data["session_info"] = {}
                data["session_info"]["uuid"] = u
                generated = True
                stats["generated_uuid"] += 1

                # Write back updated JSON file with generated UUID
                try:
                    with open(fullpath, "w", encoding="utf-8") as fw:
                        json.dump(data, fw, ensure_ascii=False, indent=2)
                    print(f"[UPDATED JSON] Wrote generated UUID to {fullpath}")
                except Exception as e:
                    print(f"[ERROR] Failed to write updated JSON to {fullpath}: {e}")

            else:
                try:
                    u = validate_uuid_str(u)
                except ValueError:
                    print(f"[WARN] Invalid UUID in {fullpath}: {u} -> generating new UUID")
                    if generate_deterministic:
                        u = str(uuid.uuid5(uuid.NAMESPACE_URL, raw))
                    else:
                        u = str(uuid.uuid4())
                    if "session_info" not in data or not isinstance(data.get("session_info"), dict):
                        data["session_info"] = {}
                    data["session_info"]["uuid"] = u
                    invalid_fixed = True
                    stats["invalid_uuid_fixed"] += 1

            if u in existing_uuids:
                print(f"[SKIP] UUID already in DB: {u} (file: {fullpath})")
                stats["skipped_already_in_db"] += 1
                continue

            si = data.get("session_info", {}) if isinstance(data, dict) else {}
            tstart = parse_time_value(si.get("time_start_unix") or si.get("time_start") or si.get("time_start_unix"))
            tend   = parse_time_value(si.get("time_end_unix")   or si.get("time_end")   or si.get("time_end_unix"))

            if tstart is None:
                try:
                    tstart = os.path.getmtime(fullpath)
                except Exception:
                    tstart = time.time()
            if tend is None:
                elapsed = si.get("time_elapsed")
                if isinstance(elapsed, (int, float)):
                    tend = tstart + float(elapsed)
                else:
                    tend = tstart + 1.0

            json_blob = json.dumps(data, ensure_ascii=False)

            try:
                cur.execute(
                    "INSERT INTO sessions (uuid, session_start_unix, session_end_unix, json_blob, report_file) VALUES (?, ?, ?, ?, ?)",
                    (u, float(tstart), float(tend), json_blob, fullpath)
                )
                conn.commit()
                existing_uuids.add(u)
                stats["inserted"] += 1
                print(f"[INSERTED] {u}  from {fullpath} (generated={generated}, invalid_fixed={invalid_fixed})")
            except sqlite3.IntegrityError:
                print(f"[SKIP DB] Integrity error on {u} (file: {fullpath})")
                stats["skipped_already_in_db"] += 1
            except Exception as e:
                print(f"[ERROR] DB insert failed for {fullpath}: {e}")
                stats["malformed_json"] += 1

    conn.close()
    print("\n=== Summary ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

    return stats


if __name__ == "__main__":
    # toggle generate_deterministic=True if you want the same UUID for identical JSON content,
    # useful to avoid duplicates when re-importing exact same files multiple times.
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("json_dir", nargs="?", default=JSON_DIR, help="Path with JSON files")
    p.add_argument("db_path", nargs="?", default=DB_PATH, help="Path to SQLite DB")
    p.add_argument("--deterministic-uuid", action="store_true", help="Generate deterministic UUIDs for files without UUID")
    args = p.parse_args()
    print("db_path=", args.db_path)
    import_json_sessions(args.json_dir, args.db_path, generate_deterministic=args.deterministic_uuid)
