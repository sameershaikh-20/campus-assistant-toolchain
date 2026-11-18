# Part D: MCP implementation and evidence

## Implementation notes

`mcp-server/server.py` uses the official Python SDK v1 `FastMCP` interface. Its stdio server exposes `get_timetable(batch, day)`, `get_fee_status(student_id)`, and the read-only `hostel://rules` resource. Function annotations and Pydantic field constraints provide the tool input schema; file access is limited to this repository's mock data. The examples below illustrate the legacy initialize lifecycle used by SDK v1 clients and Inspector. They are protocol examples, not captured server transcripts.

## Annotated JSON-RPC 2.0 examples

### 1. `initialize`

The client starts the legacy handshake and advertises a supported protocol revision. The exact negotiated revision and server metadata depend on the installed SDK.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "local-inspector", "version": "1.0.0"}
  }
}
```

Example response shape:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {"tools": {}, "resources": {}},
    "serverInfo": {"name": "Nimbus Campus Helpdesk", "version": "SDK supplied"}
  }
}
```

### 2. `tools/list`

After initialization, the client requests available tools. The input schemas shown are illustrative renderings of the Python annotations; inspect the live listing to capture the SDK's exact output.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

Example response excerpt:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_timetable",
        "description": "Return CSV timetable rows for one batch and weekday; never infer missing classes.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "batch": {"type": "string", "minLength": 1, "maxLength": 16},
            "day": {"type": "string", "enum": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
          },
          "required": ["batch", "day"]
        }
      }
    ]
  }
}
```

The live `tools/list` also includes `get_fee_status`; the excerpt is shortened for readability.

### 3. `tools/call`

This request calls the timetable tool for one batch and weekday. The result data must match the CSV.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_timetable",
    "arguments": {"batch": "CS-A", "day": "Monday"}
  }
}
```

Example successful response shape:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{"type": "text", "text": "...serialized matching rows..."}],
    "isError": false
  }
}
```

The ellipsis is explanatory placeholder text, not a captured result. Use Inspector to capture actual output if transcript evidence is required.

### 4. JSON-RPC error response

An unknown method can produce a standard JSON-RPC method-not-found error. This example illustrates the protocol error envelope; it was not captured from this server.

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

## Claimed npm package verification

The assignment asks to verify that `@nimbus/mcp-skill-bridge` version `2.3` does not exist. **Unverified:** the npm package page request was blocked (HTTP 403) in this research session, and no authoritative registry response was available. Search results alone do not prove package nonexistence, so this report does not claim that the package or version is absent. To complete this check with evidence, query the npm registry from a network-enabled environment and record the exact result and access date; do not install or execute the claimed package as part of verification.

## Sources consulted

- Official [MCP Python SDK v1 documentation](https://py.sdk.modelcontextprotocol.io/v1/) for the v1 API and legacy SDK line.
- Official [MCP Python SDK installation documentation](https://py.sdk.modelcontextprotocol.io/get-started/installation/) for the current v2 interpreter requirement and the documented `<2` compatibility bound.
- Official [MCP Python SDK resources documentation](https://py.sdk.modelcontextprotocol.io/servers/resources/) for URI-addressed resources and MIME type declaration.
- Official [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18) for JSON-RPC and the legacy lifecycle examples. The examples above are illustrative, not copied transcripts.

## Local validation status

The server source passed a Python AST syntax parse. The available `python3` in the project environment is Python 3.9, below the assignment's Python 3.10+ target, and the MCP SDK is not installed there. Therefore server startup, SDK-generated schemas, and Inspector calls remain **Unverified** in this environment. Run the README setup on Python 3.10+ to capture live protocol evidence; do not treat the illustrative payloads above as test output.
