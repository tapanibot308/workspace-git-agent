# TOOLS.md - Git Operations Guide

## Git CLI Operations

### Repository Setup

```bash
# Initialize new repository
git init [directory]

# Clone repository
git clone [url] [directory]
git clone git@github.com:TAPANIBOT/[repo].git

# Add remote
git remote add origin [url]
git remote -v  # Verify
```

### Daily Operations

```bash
# Check status
git status
git status --short  # Concise view

# Stage changes
git add [file]      # Specific file
git add .           # All changes
git add -p          # Interactive patch mode

# Commit
git commit -m "[message]"
git commit -am "[message]"  # Add and commit tracked files

# Push/pull
git push
git push -u origin [branch]  # Set upstream
git pull
```

### Branch Management

```bash
# List branches
git branch              # Local branches
git branch -r           # Remote branches
git branch -a           # All branches

# Create/switch branches
git branch [name]       # Create
git checkout [branch]   # Switch
git checkout -b [name]  # Create and switch
git switch [branch]     # Modern switch
git switch -c [name]    # Create and switch (modern)

# Merge and rebase
git merge [branch]
git rebase [branch]
git rebase -i HEAD~[n]  # Interactive rebase
```

### History & Inspection

```bash
# View log
git log
git log --oneline --graph --decorate  # Concise graph
git log -[n]                          # Last n commits

# Diff
git diff                    # Working directory vs staging
git diff --cached           # Staging vs last commit
git diff [commit] [commit]  # Between commits

# Blame
git blame [file]
```

### Stash Operations

```bash
git stash push -m "[message]"   # Save with message
git stash list                  # List stashes
git stash pop                   # Apply and remove
git stash apply                 # Apply, keep in stash
git stash drop [stash@{n}]      # Remove specific stash
```

## GitHub CLI (gh) Operations

### Repository Management

```bash
# List repositories
gh repo list [owner]
gh repo list TAPANIBOT

# Create repository
gh repo create [name] --public
git repo create [name] --private
gh repo clone [owner/repo]

# View repository
gh repo view [owner/repo]
gh repo view --web  # Open in browser
```

### Pull Requests

```bash
# Create PR
gh pr create --title "[title]" --body "[body]"
gh pr create --fill  # Use commit message

# List and view PRs
gh pr list
gh pr status
gh pr view [number]

# Checkout and manage
gh pr checkout [number]
gh pr merge [number]
gh pr merge [number] --squash
gh pr close [number]
```

### Issues

```bash
# List issues
gh issue list
gh issue list --assignee @me
gh issue list --state closed

# Create and manage
gh issue create --title "[title]" --body "[body]"
gh issue view [number]
gh issue close [number]
```

### Workflows (Actions)

```bash
# List workflows
gh workflow list

# View and trigger
gh workflow view [name]
gh workflow run [name]

# Check run history
gh run list
gh run view [id]
gh run view --log
```

### Releases

```bash
# List and create releases
gh release list
gh release create [tag] --title "[title]" --notes "[notes]"
gh release upload [tag] [file]
```

## Context7 Usage

Use Context7 for Git/GitHub API documentation lookup when needed:

```
mcp_context7_get-library-index:0
mcp_context7_resolve-library-id:1
mcp_context7_search:2
```

Use for:
- Advanced git configuration options
- GitHub API endpoint details
- Complex workflow syntax
- Error message interpretation

## Error Handling Patterns

### Before Operations

```bash
# Verify clean state
git status --porcelain
# Expected: empty output or expected changes only

# Verify correct branch
git branch --show-current
# Expected: target branch name
```

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `not a git repository` | Wrong directory | Navigate to repo root |
| `Permission denied (publickey)` | SSH auth issue | Check `gh auth status`, run `gh auth login` |
| `failed to push some refs` | Diverged branches | `git pull --rebase` then push |
| `merge conflict` | Concurrent changes | Resolve conflicts, `git add .`, `git rebase --continue` |
| `nothing to commit` | No changes staged | Check `git status`, `git diff` |

### Recovery Patterns

```bash
# Abort merge/rebase
git merge --abort
git rebase --abort

# Reset to clean state
git reset --hard HEAD

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

## Reporting Format

Always return structured results:

```markdown
## Git Operation: [operation_name]

**Status**: ✅ Success / ❌ Failed

**Repository**: `/path/to/repo`
**Branch**: `main`
**Commit**: `abc1234`

**Details**:
- File 1: modified
- File 2: added
- File 3: deleted

**Command Output**:
```
[relevant output]
```

**Next Steps**:
- [ ] Action 1
- [ ] Action 2
```

## Quick Reference

| Task | Command |
|------|---------|
| What's changed? | `git status --short` |
| What did I just commit? | `git show --stat` |
| Where am I? | `git branch --show-current` |
| What's the remote URL? | `git remote get-url origin` |
| Who am I on GitHub? | `gh auth status` |
