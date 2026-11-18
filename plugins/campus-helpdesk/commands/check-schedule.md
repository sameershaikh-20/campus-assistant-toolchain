---
description: Look up a batch's classes for a specified weekday from the campus CSV.
argument-hint: <batch> <weekday>
---

Check the campus schedule for `$ARGUMENTS`.

Use the `get_timetable` MCP tool or the bundled `timetable-helper` skill to look up those exact values in the repository timetable CSV. If the batch or weekday is missing or unclear, ask one short clarifying question. Report only rows returned from the CSV. If there are no matches, say so clearly; never create a class, room, time, or instructor.
