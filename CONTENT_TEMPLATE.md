---
title: Your Title Here
platform: TryHackMe
difficulty: easy
date: 2026-01-20
tags: [tag1, tag2, tag3]
summary: A one-sentence summary that shows on the card and at the top of the article.
---

# Your Title Here

Write your content in standard markdown below. Everything here gets rendered.

## A section heading

Normal paragraph text. You can use **bold**, *italic*, `inline code`, and [links](https://example.com).

> Use blockquotes for important callouts or key takeaways.

## Code blocks

```bash
grep -r "error" /var/log/
```

## Tables

| Column A | Column B |
|----------|----------|
| value 1  | value 2  |
| value 3  | value 4  |

## Lists

- First point
- Second point
- Third point

---

## Frontmatter field reference

The block between the `---` lines at the top is the "frontmatter". Fields:

- **title** — required. The display title.
- **platform** — optional. Shows as a badge (e.g. TryHackMe, LetsDefend).
- **difficulty** — optional. One of: easy, medium, hard. Shows as a coloured tag.
- **date** — optional but recommended. Format YYYY-MM-DD. Used for sorting.
- **tags** — optional. Comma-separated list in square brackets.
- **summary** — optional. One-sentence description shown on cards.

For **certs**, use `status: passed` / `studying` / `planned` and `org: CompTIA` instead of platform/difficulty.
