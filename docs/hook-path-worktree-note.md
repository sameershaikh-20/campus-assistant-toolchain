# Protected-file hook path review

This independent `bugfix/hook-path` change records the path-resolution expectations reviewed for the guard. Direct file-tool paths should be rejected when a normalized path contains an exact `data` or `.claude-plugin` component, whether the tool supplies a relative or absolute path. The hook also normalizes backslashes to slashes before checking components. Bash checks are intentionally more conservative: a literal protected component anywhere in the command is denied.

The guard is defense in depth only. Symlinks, variables, encoded paths, unrecognized tools, and non-Claude processes require filesystem or sandbox controls rather than a shell substring hook.
