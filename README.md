# Nimbus Labs Campus Helpdesk Toolchain

A local academic project for the fictional Nimbus Labs campus helpdesk. It demonstrates a grounded timetable Skill, a Claude Code plugin bundle, a Python MCP server over stdio, and parallel Git worktree development. All student, fee, schedule, instructor, and hostel information in this repository is original mock data.

## Project map

| Area | Contents |
| --- | --- |
| Mock data | `data/timetable.csv`, `data/fee_status.json`, `data/hostel_rules.md` |
| Timetable Skill | `skills/timetable-helper/` with schema and edge-case references plus deterministic lookup script |
| Plugin | `plugins/campus-helpdesk/` with a bundled Skill, `/campus-helpdesk:check-schedule`, a protected-path hook, and local MCP configuration |
| MCP server | `mcp-server/server.py` exposes timetable and fee tools plus `hostel://rules` |
| Assignment evidence | `docs/part-a-claim-audit.md`, `docs/part-b-skill-tests.md`, `docs/part-c-plugin-and-security.md`, `docs/part-d-mcp-evidence.md`, `docs/part-e-worktrees.md`, `docs/part-f-reflection-and-log.md` |

## Local setup

The assignment targets Python 3.10 or newer. Create an environment and install the MCP Python SDK v1 range:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r mcp-server/requirements.txt
```

Run the timetable lookup from the repository root:

```bash
python3 skills/timetable-helper/scripts/lookup_timetable.py --batch CS-A --day Monday
```

Run the MCP stdio server for a compatible client:

```bash
python mcp-server/server.py
```

For setup details and the local MCP Inspector command, see [`mcp-server/README.md`](mcp-server/README.md). Inspector may need to download its package through `npx` the first time; no paid API or cloud service is used by the project.

## Cost and runtime notes

The Python MCP server and Inspector use open-source tools and do not call a paid API. The Claude Code plugin files are included to meet the assignment's packaging requirements, but running them through Claude Code requires access to Claude Code, which Anthropic currently includes with paid plans. You can clone, inspect, and test the local MCP server without using Claude Code; plugin runtime behavior remains unverified here.

## What is verified locally

- The timetable lookup returned two CSV-backed rows for CS-A on Monday and no rows for CS-A on Thursday.
- The hook passed shell syntax checking and denied sample direct-write and Bash inputs that referenced protected paths.
- The Git worktree exercise created and merged the three named branches, resolved an add/add conflict, recorded the history, and removed the linked worktree directories without force.
- The Part A audit records official sources and an access date. Claim 10 remains Unverified; an arXiv no-result query does not prove the cited paper is nonexistent.

The MCP server and Claude Code plugin were not run in this environment: available Python is 3.9, the MCP SDK is not installed, and the Claude Code CLI is unavailable. The MCP examples are explicitly marked illustrative, not captured protocol transcripts. The npm existence check for `@nimbus/mcp-skill-bridge@2.3` also remains Unverified because the npm package-page request was blocked; do not cite it as a verified absence.

## Git state

The base project and worktree exercise are committed on `main`. Feature branches remain in history after the temporary linked worktree directories were safely removed. Use `git worktree list` to inspect the current checkout list and `git log --graph --oneline --decorate --all` to review the merge history.

## Scope

This repository provides mock data and local integration code only. The MCP tools are read-only; no live student system, payment processor, or institutional service is connected.
