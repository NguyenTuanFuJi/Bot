---
name: wordpress-cli-app-password
description: Operate WordPress content through REST API with Application Password or WP-CLI when available. Use when the user wants to create, update, schedule, publish, or review WordPress posts, run safe preflight checks, manage SEO fields, or choose the correct publishing path for a WordPress site.
---

# WordPress Ops

Use this skill to publish and maintain WordPress content safely.

## Operating modes

### REST API + Application Password
Use this as the default mode.
Best for:
- remote publishing
- content operations
- scheduled post updates
- SEO field updates

### WP-CLI
Use only when preflight confirms it is available and appropriate.
Best for:
- server-side operations
- deeper WordPress admin work
- environments that already expose WP-CLI reliably

## Credentials
Primary env file:
- `skills/wordpress-cli-app-password/.env`

If credentials are missing or invalid, update that env file before continuing.

## Required workflow

1. Run triage
```bash
bash scripts/wp_triage.sh <project_root>
```

2. Choose mode
- `rest`
- `wpcli`

3. Run preflight
```bash
bash scripts/wp_ops.sh preflight --env .env --mode rest
bash scripts/wp_ops.sh preflight --env .env --mode wpcli
```

4. Only create / update / publish after preflight passes

## Common commands

### REST post operations
```bash
bash scripts/wp_posts.sh create --env .env --title "Tiêu đề" --content-file ./post.html --status draft
bash scripts/wp_posts.sh update --env .env --id 123 --status publish
bash scripts/wp_posts.sh list --env .env --per-page 10
```

### Unified entrypoint
```bash
bash scripts/wp_ops.sh create --env .env --mode rest --title "Tiêu đề" --content-file ./post.html --status draft
bash scripts/wp_ops.sh update --env .env --mode rest --id 123 --status publish
bash scripts/wp_ops.sh preflight --env .env --mode rest
```

## SEO and publishing rules
- Prefer draft before publish unless the user wants immediate publishing
- Do not expose secrets from `.env`
- Run the Yoast checklist before publishing SEO-managed content
- Optimize slug, focus keyphrase, SEO title, and meta description when relevant
- Add internal links and image metadata when the workflow requires SEO completion

## Read references when needed
- `references/wordpress-content-workflow.md`
- `references/wp-safe-checklist.md`
- `references/yoast-seo-fujith-playbook.md`
- `references/wpcli-quick-ops.md`
- `references/wpcli-safe-ops.md`

## Result format
Return briefly:
- status
- post ID / URL / publish state
- next recommended action

Use this skill for WordPress publishing operations. Use content-generation or content-strategy for the writing and planning itself.