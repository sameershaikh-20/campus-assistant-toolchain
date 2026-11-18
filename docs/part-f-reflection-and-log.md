# Part F: reflection and prompt log

## Prompt log template

The assignment requires at least five verified entries where an AI answer was wrong or unverifiable. Record exact outputs from your own AI sessions and attach the evidence used to check them. Do not fill a row from memory or invent a transcript; an empty row is a prompt to collect evidence, not a completed log entry.

| Entry | Date / tool / model | Exact prompt and relevant AI answer | Verification source or command | Finding (wrong / unverified / correct) | Correction or rejection |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Suggested verification workflow

1. Save the exact prompt and answer before editing it.
2. Identify the factual or command claim that can be checked.
3. Prefer the relevant official specification, vendor documentation, or authoritative registry.
4. Record the command/output or direct source passage and access date.
5. Mark an absence-of-evidence result Unverified; do not turn a failed search into proof of nonexistence.

## Reflection draft (approximately 300 words)

The four mechanisms in this project solve different problems. A Skill packages reusable instructions for a narrow task: `timetable-helper` tells an agent how to interpret the CSV, ask for missing details, and avoid inventing schedule rows. A plugin packages related components for a particular host; the campus-helpdesk plugin bundles that skill with a command, a hook, and MCP configuration. The plugin is a distribution unit, while the Skill is domain guidance.

MCP provides a protocol boundary between an agent host and local data or actions. In this project, the timetable and fee tools perform structured lookups, and the hostel rules are exposed as a read-only resource. The mock records remain the source of truth. A Skill is the better choice when the agent needs procedural guidance, response rules, or a workflow that uses existing files and tools. An MCP tool is preferable when the host needs a well-defined operation or fresh structured data through a typed interface.

Git worktrees address a different concern: they let parallel work happen in separate directories while sharing repository history. The three feature branches could change their own files independently, and the shared new file produced a real add/add conflict. Git reported the conflict, but a person still had to decide how to combine both changes. This illustrates that mechanical conflict resolution does not establish that the result is correct.

I would not delegate approval of consequential actions without review. In particular, an agent should not independently merge changes affecting student records, alter real fee balances, change access controls, or publish a release. Those actions require a human to inspect the evidence, diff, and expected impact. The same principle applies to tool descriptions, hooks, and instructions: they shape agent behavior and deserve review before use. The project’s mock data and read-only tools keep this demonstration bounded, but they do not replace review in a real campus system.
