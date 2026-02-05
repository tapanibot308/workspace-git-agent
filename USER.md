# USER.md - User Context

## Identity

- **Name**: Jussi
- **Company**: Skycode Oy / SkyPlanner

## GitHub Configuration

| Account | Purpose |
|---------|---------|
| **TAPANIBOT** | Primary organization account for all work repositories |
| **tapanibot308** | Personal account (login only, not for active development) |

## Preferences

| Preference | Value |
|------------|-------|
| **Communication** | Efficiency over verbosity |
| **Chatter** | No unnecessary small talk |
| **Timezone** | Europe/Helsinki (EET/EEST) |

## Implications for Git Operations

- Default to TAPANIBOT organization for new repositories
- Use SSH keys for authentication (check `git remote -v` output)
- Respect Helsinki timezone for commit timestamps when relevant
- Skip confirmation prompts for routine operations

## Common Patterns

```bash
# Default clone pattern
git clone git@github.com:TAPANIBOT/[repo].git

# Check current remotes
git remote -v

# Verify correct account for operations
gh auth status
```
