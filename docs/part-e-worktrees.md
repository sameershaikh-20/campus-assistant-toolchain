# Part E: parallel development with Git worktrees

## 1. Create and list linked worktrees

The base project was committed on `main` as `ee71ef6` (`Build campus helpdesk toolchain base`). Three linked worktrees were created from that commit in a writable temporary directory outside the repository:

```bash
git worktree add /private/tmp/campus-assistant-toolchain-worktrees/skill-tests -b feature/skill-tests main
git worktree add /private/tmp/campus-assistant-toolchain-worktrees/mcp-server -b feature/mcp-server main
git worktree add /private/tmp/campus-assistant-toolchain-worktrees/hook-path -b bugfix/hook-path main
git worktree list
```

Captured `git worktree list` output after all three workstreams were merged, before removing their linked directories:

```text
<repository-root>                                             dcfd128 [main]
/private/tmp/campus-assistant-toolchain-worktrees/hook-path   8d53484 [bugfix/hook-path]
/private/tmp/campus-assistant-toolchain-worktrees/mcp-server  ad48379 [feature/mcp-server]
/private/tmp/campus-assistant-toolchain-worktrees/skill-tests 33eaad6 [feature/skill-tests]
```

## 2. Independent changes and conflict resolution

Each linked worktree received a separate change and commit:

- `feature/skill-tests`: `33eaad6 Add skill test worktree note`
- `feature/mcp-server`: `ad48379 Add MCP worktree documentation`
- `bugfix/hook-path`: `8d53484 Document hook path handling`

The first two branches independently added `docs/worktree-conflict-demo.md`, which caused a real add/add conflict when the second branch was merged. The recorded sequence was:

```bash
git merge --no-ff feature/skill-tests -m "Merge skill test workstream"
git merge --no-ff feature/mcp-server -m "Merge MCP server workstream"
# Git reported: CONFLICT (add/add): Merge conflict in docs/worktree-conflict-demo.md
# Resolve the file manually, keeping both branches' notes, then:
git add docs/worktree-conflict-demo.md
git commit -m "Resolve worktree documentation conflict"
git merge --no-ff bugfix/hook-path -m "Merge hook path workstream"
```

This is the captured `git log --graph --oneline --decorate --all` output after resolving and merging the three branches, before adding this report:

```text
*   dcfd128 (HEAD -> main) Merge hook path workstream
|\
| * 8d53484 (bugfix/hook-path) Document hook path handling
* |   514fe91 Resolve worktree documentation conflict
|\ \
| * | ad48379 (feature/mcp-server) Add MCP worktree documentation
| |/
* |   a9c481a Merge skill test workstream
|\ \
| |/
|/|
| * 33eaad6 (feature/skill-tests) Add skill test worktree note
|/
* ee71ef6 Build campus helpdesk toolchain base
```

The resolved file states why Git conflicted and that both branches' information was retained. The merge was reviewed manually rather than delegated without review.

## 3. Worktree concepts

**(a) Why Git refuses the same branch in two worktrees.** By default, Git prevents one branch from being checked out in multiple worktrees. This avoids two independent working directories both appearing to represent the same branch tip and prevents updates from one checkout from making the other checkout ambiguous or unsafe. Git has a force option, but ordinary parallel work should use one branch per worktree.

**(b) What is shared and what is separate.** Worktrees share the repository's object database and most refs/history, along with the common repository configuration by default. Each worktree has its own checked-out files and per-worktree state such as `HEAD` and the index; its `.git` entry is a pointer file to Git's shared administration area. Untracked or ignored local files such as `node_modules/` and `.env` are not copied into a newly added worktree. Create/install them separately or deliberately manage a safe shared cache; do not assume they are present.

**(c) Cleaning up safely.** First run `git worktree list`, check each candidate with `git -C <path> status --short --branch`, and confirm its work is committed or merged. Then use `git worktree remove <path>` without `--force`; it refuses a dirty worktree. If a directory was manually deleted, preview stale metadata with `git worktree prune --dry-run`, then run `git worktree prune`. Removing a worktree does not by itself delete its branch; inspect branches and decide separately whether they are still useful.

Git's documentation explains that branch checkout is refused by default when that branch is already checked out in another worktree, and that linked worktrees share repository data except per-worktree state such as `HEAD` and the index. It also documents `remove` and `prune` for cleanup. [Git worktree documentation](https://git-scm.com/docs/git-worktree)

### Cleanup performed

After verifying that each linked worktree was clean and its branch was merged, the three temporary working directories were removed without `--force`. Since Git removed their administrative records normally, the prune preview had no stale entries. The final list contains only the main worktree:

```bash
git worktree remove /private/tmp/campus-assistant-toolchain-worktrees/skill-tests
git worktree remove /private/tmp/campus-assistant-toolchain-worktrees/mcp-server
git worktree remove /private/tmp/campus-assistant-toolchain-worktrees/hook-path
git worktree prune --dry-run
git worktree list
```

```text
<repository-root> abf1cbd [main]
```

## 4. Evaluate the CTO's `/worktree-merge` claim

**Verdict: false as a claim about a built-in Claude Code command.** On 2026-11-18, the official Claude Code [Commands reference](https://code.claude.com/docs/en/commands) was checked: it documents built-in commands and bundled skills, includes worktree-related `/batch`, and has no `/worktree-merge` entry. This check establishes that the command is not documented as a built-in command; it cannot rule out a custom skill or plugin someone has named that way. The official guide describes `/batch` as running work in isolated worktrees, not as automatically resolving Git conflicts without review.

Letting an agent create a merge commit without human review risks losing one branch's behavior, accepting a semantically invalid resolution, or merging unsafe code even when Git reports no textual conflict. Review the diff and tests, inspect the merge parents, and verify the resulting behavior before accepting the merge.
