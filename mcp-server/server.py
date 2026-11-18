"""Local, read-only campus helpdesk MCP server over stdio."""

import csv
import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field
from mcp.server.fastmcp import FastMCP


ROOT = Path(__file__).resolve().parents[1]
TIMETABLE_PATH = ROOT / "data" / "timetable.csv"
FEE_STATUS_PATH = ROOT / "data" / "fee_status.json"
HOSTEL_RULES_PATH = ROOT / "data" / "hostel_rules.md"
WEEKDAYS = Literal[
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

mcp = FastMCP("Nimbus Campus Helpdesk")


@mcp.tool()
def get_timetable(
    batch: Annotated[str, Field(min_length=1, max_length=16, pattern=r"^[A-Za-z0-9-]+$")],
    day: WEEKDAYS,
) -> dict[str, object]:
    """Return CSV timetable rows for one batch and weekday; never infer missing classes."""
    try:
        with TIMETABLE_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"batch", "day", "time_slot", "course_code", "course_name", "room", "instructor"}
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)) or not required.issubset(headers):
                return {"error": "Timetable CSV has an invalid header."}
            matches = [
                row for row in reader
                if (row.get("batch") or "").strip().casefold() == batch.strip().casefold()
                and (row.get("day") or "").strip().casefold() == day.casefold()
            ]
        return {"batch": batch, "day": day, "matches": matches}
    except (OSError, UnicodeError, csv.Error) as exc:
        return {"error": f"Could not read timetable data: {exc.__class__.__name__}."}


@mcp.tool()
def get_fee_status(
    student_id: Annotated[str, Field(min_length=1, max_length=24, pattern=r"^[A-Za-z0-9-]+$")],
) -> dict[str, object]:
    """Return the mock fee record for one exact student ID; disclose no other records."""
    try:
        with FEE_STATUS_PATH.open("r", encoding="utf-8") as handle:
            records = json.load(handle)
        if not isinstance(records, list):
            return {"error": "Fee status data must be a JSON array."}
        for record in records:
            if isinstance(record, dict) and record.get("student_id", "").casefold() == student_id.casefold():
                return record
        return {"error": "No fee record found for that student ID."}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"error": f"Could not read fee status data: {exc.__class__.__name__}."}


@mcp.resource("hostel://rules", mime_type="text/markdown")
def hostel_rules() -> str:
    """Read the campus hostel rules document."""
    try:
        return HOSTEL_RULES_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return f"Hostel rules are unavailable ({exc.__class__.__name__})."


if __name__ == "__main__":
    # stdio is the default transport for local MCP clients. Keep stdout reserved
    # for protocol messages; do not add print-based logging here.
    mcp.run(transport="stdio")
