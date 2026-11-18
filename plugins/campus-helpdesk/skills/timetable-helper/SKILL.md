---
name: timetable-helper
description: Use when a student asks for scheduled classes, course times, rooms, or instructors for a batch on a particular day, using the campus timetable CSV. Do not use for fees, hostel rules, course advice, or general calendar questions.
---

# Timetable helper

Answer timetable questions only from the supplied `data/timetable.csv`.

- Identify the requested batch and day. If either is missing or unclear, ask a concise clarifying question.
- Use the CSV lookup script or inspect the CSV directly; report only matching rows.
- If no row matches, say that the CSV has no listed classes for that batch and day. Never invent, infer, or substitute a class, room, time, or instructor.
- See [CSV schema](references/csv-schema.md) and [edge cases](references/edge-cases.md) for field meanings and handling rules.
