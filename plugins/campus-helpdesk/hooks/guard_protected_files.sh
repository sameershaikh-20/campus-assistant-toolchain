#!/usr/bin/env bash
# Conservative PreToolUse guard. Literal references to protected path
# components in Bash commands are blocked, including read-only references.
set -euo pipefail

payload="$(cat)"
decision="$(python3 -c '
import json
import re
import sys

try:
    event = json.loads(sys.argv[1])
except (IndexError, json.JSONDecodeError):
    # Fail closed if the hook cannot inspect its input.
    print("deny:invalid hook input")
    raise SystemExit(0)

tool = event.get("tool_name", "")
tool_input = event.get("tool_input") or {}
protected = {"data", ".claude-plugin"}

def contains_protected_component(value):
    if not isinstance(value, str):
        return False
    normalized = value.replace("\\", "/")
    return any(part in protected for part in normalized.split("/"))

if tool in {"Write", "Edit", "NotebookEdit"}:
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if contains_protected_component(path):
        print("deny:protected file path")
        raise SystemExit(0)
elif tool == "Bash":
    command = tool_input.get("command", "")
    # Deliberately block any literal protected path component in a Bash call.
    # Parsing arbitrary shell safely is not possible with a simple hook.
    if re.search(r"(?<![A-Za-z0-9_.-])(?:data|\.claude-plugin)(?![A-Za-z0-9_.-])", command):
        print("deny:protected path mentioned in Bash command")
        raise SystemExit(0)

print("allow")
' "$payload")"

case "$decision" in
  deny:*)
    reason="${decision#deny:}"
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Campus helpdesk guard blocked %s."}}\n' "$reason"
    ;;
  allow)
    exit 0
    ;;
  *)
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Campus helpdesk guard could not validate this request."}}\n'
    ;;
esac
