---
name: facebook-page
description: Manage Facebook Pages through Meta Graph API. Use when the user wants to publish a Facebook post, post photos or links, list page posts, review or manage comments, check page access, or schedule Facebook publishing through the workspace automation flow.
---

# Facebook Page

Use this skill to operate Facebook Pages safely through the existing scripts and credentials in this skill folder.

## Main use cases
- List managed pages
- Publish text posts
- Publish photo posts or albums
- Publish link posts
- List recent posts
- List, reply to, hide, or delete comments
- Run cron-safe Facebook posting

## Profiles and credentials
This skill uses profile-specific credentials.
Common profiles:
- `facebook_fujith`
- `facebook_app2`

Use the matching credential files under:
- `credentials/<profile>/.env`
- `credentials/<profile>/tokens.json`

When running commands, set `FB_PROFILE` explicitly to avoid using the wrong Page credentials.

## Normal workflow

1. Pick the correct profile
2. Run preflight before important posting jobs
3. Publish with the existing CLI or cron-safe wrapper
4. Confirm the post result or capture the error
5. Report the post link or next action

## Commands

### List pages
```bash
FB_PROFILE=facebook_fujith node scripts/cli.js pages
```

### Create post
```bash
FB_PROFILE=facebook_fujith node scripts/cli.js post create --page PAGE_ID --message "Caption"
```

### Create post with photo
```bash
FB_PROFILE=facebook_fujith node scripts/cli.js post create --page PAGE_ID --message "Caption" --photo /abs/path/image.jpg
```

### List posts
```bash
FB_PROFILE=facebook_fujith node scripts/cli.js post list --page PAGE_ID --limit 10
```

### Comment operations
```bash
FB_PROFILE=facebook_fujith node scripts/cli.js comments list --post POST_ID
FB_PROFILE=facebook_fujith node scripts/cli.js comments reply --comment COMMENT_ID --message "Thanks"
FB_PROFILE=facebook_fujith node scripts/cli.js comments hide --comment COMMENT_ID
FB_PROFILE=facebook_fujith node scripts/cli.js comments delete --comment COMMENT_ID
```

## Cron-safe posting
Use the wrapper scripts when scheduling via cron.

### Preflight
```bash
bash scripts/preflight.sh
```
Expect `PRECHECK_OK` before scheduling.

### Wrapper commands
```bash
FB_PROFILE=facebook_fujith bash scripts/cron-safe-post.sh --page PAGE_ID --message-file /abs/path/message.txt --photo /abs/path/image.jpg

FB_PROFILE=facebook_fujith bash scripts/cron-safe-post-album.sh --page PAGE_ID --message-file /abs/path/message.txt --photo /abs/1.jpg --photo /abs/2.jpg
```

## Rules
- Use absolute paths for cron jobs
- Do not print tokens in output
- Prefer `FB_PROFILE` explicitly on every operational command
- Run preflight before cron scheduling or bulk posting
- Use the references folder for content quality guidance, not SKILL.md

## Read references when needed
- `references/facebook-seo-content-v2.md`

Use this skill for Page operations. Use `facebook-content-ops` when the user wants planning, content backlog, or KPI/process guidance.