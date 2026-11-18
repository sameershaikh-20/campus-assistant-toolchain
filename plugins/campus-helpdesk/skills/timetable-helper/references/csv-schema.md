# Timetable CSV schema

The source file is `data/timetable.csv`, encoded as UTF-8 with a header row. Each data row represents one scheduled class. Preserve the source values when answering; do not fill blanks or normalize a course into a different course.

| Column | Meaning | Handling |
| --- | --- | --- |
| `batch` | Class cohort, such as `CS-A`, `CS-B`, or `AI-DS` | Match the requested batch without treating one batch as another. |
| `day` | Weekday on which the class is scheduled | Match a recognized day name; case differences may be ignored. |
| `time_slot` | Start and end time as stored in the CSV | Quote the stored value; do not convert time zones. |
| `course_code` | Course identifier | Report exactly as stored. |
| `course_name` | Course title | Report exactly as stored. |
| `room` | Room or lab location | Report exactly as stored. |
| `instructor` | Instructor name and title | Report exactly as stored. |

Rows are independent. More than one row may exist for the same batch and day; return every matching row in CSV order. The header names are required. Missing or duplicate required headers make the file invalid for lookup.
