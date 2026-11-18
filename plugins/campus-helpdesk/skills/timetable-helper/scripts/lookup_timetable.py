#!/usr/bin/env python3
"""Deterministically look up classes in the project timetable CSV."""

import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED_COLUMNS = (
    "batch",
    "day",
    "time_slot",
    "course_code",
    "course_name",
    "room",
    "instructor",
)
DEFAULT_CSV = Path(__file__).resolve().parents[3] / "data" / "timetable.csv"


def lookup(csv_path: Path, batch: str, day: str) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)):
            raise ValueError("CSV contains duplicate column names")
        missing = [column for column in REQUIRED_COLUMNS if column not in headers]
        if missing:
            raise ValueError("CSV is missing required columns: " + ", ".join(missing))

        matches = []
        for row in reader:
            if None in row:
                raise ValueError("CSV row has more values than the header")
            if (row["batch"].strip().casefold() == batch.strip().casefold()
                    and row["day"].strip().casefold() == day.strip().casefold()):
                matches.append({column: (row[column] or "").strip() for column in REQUIRED_COLUMNS})
        return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up classes by batch and day.")
    parser.add_argument("--batch", required=True, help="Batch label, for example CS-A")
    parser.add_argument("--day", required=True, help="Full weekday name, for example Monday")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Timetable CSV path")
    args = parser.parse_args()

    try:
        matches = lookup(args.csv, args.batch, args.day)
    except FileNotFoundError:
        print(f"Error: timetable CSV not found: {args.csv}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"Error: cannot read timetable CSV: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"batch": args.batch, "day": args.day, "matches": matches}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
