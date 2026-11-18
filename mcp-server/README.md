# Local campus helpdesk MCP server

This server uses the official MCP Python SDK and serves local mock data only. It exposes two tools (`get_timetable` and `get_fee_status`) plus the read-only `hostel://rules` resource. It makes no API or cloud calls.

## Requirements and setup

Use Python 3.10 or newer with a compatible release of the SDK's v1 line. The current SDK documentation describes v2 as the stable line and lists Python 3.11+; this project bounds the dependency below v2 to preserve the assignment's Python 3.10+ target and the v1 API used here. Confirm the Python version and install the pinned range:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r mcp-server/requirements.txt
```

## Run locally

From the repository root:

```bash
python mcp-server/server.py
```

The process speaks MCP over stdio and waits for a client. Do not type shell commands into that process. The SDK owns stdout for protocol traffic; the server has no stdout logging.

## MCP Inspector

With the virtual environment active, launch the local server through Inspector:

```bash
npx -y @modelcontextprotocol/inspector python mcp-server/server.py
```

Choose the stdio connection in Inspector. Test `get_timetable` with `{"batch":"CS-A","day":"Monday"}` and with `{"batch":"CS-A","day":"Thursday"}`; the former returns CSV rows and the latter an empty match list. Test `get_fee_status` with `{"student_id":"STU202602"}` and read `hostel://rules`.

The command is included for a local Inspector session; `npx` may obtain the Inspector package on first use, so this step needs a network connection if it is not already cached. No paid API or service is used.

## Tool input schemas

The SDK derives JSON Schema from the typed function signatures. Both tool inputs are required objects with constrained string fields; `day` is limited to the seven weekday names. Invalid schema values are rejected during input validation. A syntactically valid but unknown batch or student ID receives a small JSON error object. The tools return only matching timetable rows or the requested student's fee record.

For annotated JSON-RPC 2.0 request/response examples and verification notes, see [`docs/part-d-mcp-evidence.md`](../docs/part-d-mcp-evidence.md).
