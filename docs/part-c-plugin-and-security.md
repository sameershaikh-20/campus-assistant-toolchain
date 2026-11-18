# Part C: campus-helpdesk plugin and security

## Bundle contents

The Claude Code plugin is in `plugins/campus-helpdesk/`. It contains a copy of the `timetable-helper` skill and its references/script, the `/campus-helpdesk:check-schedule` command, a `PreToolUse` guard, and an MCP configuration for the repository's `mcp-server/server.py`. The root `.claude-plugin/marketplace.json` catalogs the plugin as a local relative-path source.

The `.mcp.json` uses `${CLAUDE_PROJECT_DIR}` to point at this checkout's server. This makes the plugin configuration repository-specific: install and use it from this project root, after installing the Python requirements. The Python MCP server remains a separate project path rather than being copied into the plugin package.

## Validate, add, install, verify, uninstall

The commands below follow the official Claude Code plugin CLI. The local marketplace must be added from the repository root because it contains `.claude-plugin/marketplace.json`. Marketplace registration and plugin installation are user-level operations unless a scope is specified; these commands explicitly choose project scope for the plugin installation.

```bash
# Check the plugin's manifest, component paths, hook, and MCP config.
claude plugin validate ./plugins/campus-helpdesk

# Register the local marketplace from this repository root.
claude plugin marketplace add ./

# Install the catalog entry for this project.
claude plugin install campus-helpdesk@nimbus-campus-local --scope project

# Inspect installation state and plugin metadata.
claude plugin list
claude plugin details campus-helpdesk@nimbus-campus-local
```

In a Claude Code session, `/plugin` opens the plugin manager. The skill is namespaced under the plugin, and the command is `/campus-helpdesk:check-schedule`. Use `/mcp` to inspect whether `campus-helpdesk-data` connected. `claude plugin validate` validates configuration, not the behavior of the guard or actual MCP tool calls; those require runtime checks.

To uninstall only the plugin and leave the marketplace registered:

```bash
claude plugin uninstall campus-helpdesk@nimbus-campus-local --scope project
```

To remove the marketplace registration as well, run this separate command. The official docs state that removing a marketplace also uninstalls every plugin installed from it:

```bash
claude plugin marketplace remove nimbus-campus-local
```

These Claude Code commands depend on Claude Code being installed. Anthropic currently includes Claude Code with paid plans, so running this plugin through Claude Code may require a paid subscription. The commands are documented because the assignment asks for Claude Code plugin CLI steps; the plugin itself does not call a paid API, and the local Python MCP server can be used independently.

## Protected-file hook behavior

`PreToolUse` runs before `Write`, `Edit`, `NotebookEdit`, and `Bash`. The shell script reads the hook JSON from stdin and returns the documented `permissionDecision: "deny"` response when a direct file tool's path contains a `data` or `.claude-plugin` component. For Bash it conservatively denies any command containing either literal path component, including reads. It emits no decision for other inputs, allowing the normal permission flow to continue. The script is executable in the repository.

This is a teaching safeguard, not a complete security boundary. Shell parsing is not safely reducible to a few string checks: aliases, variables, encoded paths, symlinks, other tools, other processes, or edits outside Claude Code can bypass it. For actual integrity guarantees, enforce filesystem permissions or use a sandbox with those directories mounted read-only, and test adversarial paths. Avoid expanding the hook to execute arbitrary model-supplied shell text.

## Threat model and mitigations

| Threat | Example impact | Mitigations in this project |
| --- | --- | --- |
| Prompt injection through Skill text | A malicious instruction inside a skill or reference asks the agent to ignore grounding rules, reveal private records, or run commands. | Treat data and skill text as untrusted instructions; follow the top-level task policy; read class facts only from the CSV; never follow embedded requests to invent records. Keep the skill narrowly scoped and review changes to it. |
| Malicious shell hook | A hook can run with the user's permissions and could exfiltrate files, delete data, or alter the environment. | The bundled hook is a short local script with no network calls, no writes, and no dynamic command execution. Inspect the script and hook registration before enabling the plugin; keep the script in version control and restrict file permissions. |
| Tool poisoning through MCP descriptions | A misleading tool description could induce the model to disclose extra data, call the wrong tool, or trust unverified output. | Use clear, bounded descriptions; expose only read-only tools/resources; constrain tool schemas; return a single student's fee record by exact ID; disclose no other records; verify results against mock files and inspect live `tools/list` metadata. Treat tool output as data, not instructions. |

The shell hook's literal path checks are bypassable and should not be described as enforcing OS-level immutability. The strongest mitigation for protected files is filesystem-level read-only access; the hook is a defense-in-depth demonstration.

## Sources

- Official [Claude Code plugin creation guide](https://code.claude.com/docs/en/plugins/create) and [plugin components reference](https://code.claude.com/docs/en/plugins/components) for layout, commands, hooks, and validation.
- Official [plugin marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) and [install/manage guide](https://code.claude.com/docs/en/plugins/install) for local marketplace sources and CLI commands.
- Official [hooks reference](https://code.claude.com/docs/en/hooks) for PreToolUse stdin and deny output.
- Official [MCP configuration guide](https://code.claude.com/docs/en/mcp) for plugin `.mcp.json` and `${CLAUDE_PROJECT_DIR}` expansion.
