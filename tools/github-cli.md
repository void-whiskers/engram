---
status: current
created: 2026-08-26
updated: 2026-08-26
tags: [tools, github, gh, cli, authentication]
---

# GitHub CLI (`gh`)

The GitHub CLI is one of several ways agents interact with GitHub (alongside MCP servers and the REST/GraphQL APIs). This document covers the authentication workflow agents must follow when using `gh` directly.

## Verifying authentication

Before any `gh` operation, check that the CLI is installed and authenticated:

```bash
gh --version
gh auth status
```

If both succeed, proceed normally. If `gh auth status` fails, follow the device-login flow below before continuing.

## Device-login flow

Start GitHub's device-login flow without opening a local browser:

```bash
GH_BROWSER=echo gh auth login --hostname github.com --git-protocol ssh --skip-ssh-key
```

This command:

- preserves SSH as the Git transport protocol;
- suppresses the SSH-key upload prompt (the user manages their own keys); and
- prints the device-login URL to stdout instead of launching a browser.

When `gh` presents the **one-time device code** and **verification URL**, relay both to the user in chat and ask them to complete the approval in their browser. Device codes are short-lived and may be shared only with the user who requested authentication.

Keep the authentication command running until the user reports they have completed the browser approval, then verify the session.

## Verifying after approval

```bash
gh auth status
gh api user --jq .login
```

Proceed only when both commands succeed. If authentication still fails, report the exact non-sensitive error and leave credential repair to the user.

## Headless environments

In environments with no browser access, the user may supply `GH_TOKEN` through the platform's secret mechanism, or run `gh auth login --with-token` directly in their own terminal. The agent must not receive, store, or handle the token.

## Credential safety

Agents MUST NOT:

- print, read, copy, or request a token in chat, command output, logs, patches, or environment inspection;
- store tokens in files, environment variables, or commit history; or
- automate browser interaction during the login flow.

Device codes are the only authentication artefact an agent may share, and only with the user who initiated the flow.
