# Security Policy

## Why a Markdown repository has one

Engram contains no application code, but agents act on it. `AGENTS.md` and the skills in `.agents/skills/` are instructions that AI agents with shell and git access follow on your machine, and the validation scripts run locally and in CI. A change that makes an agent run a harmful command, send data somewhere, or weaken a safety rule is a security issue, even though it is only text.

## Supported Versions

The latest commit on `main` is the supported version. Fixes are not back-ported to earlier tags.

A repository created from this template is a copy: it does not receive fixes automatically. Security fixes are described in the release notes so that you can apply them to your own copy.

## Reporting a Vulnerability

Use GitHub private vulnerability reporting:

1. Open the **Security** tab of the [`void-whiskers/engram`](https://github.com/void-whiskers/engram) repository.
2. Click **Report a vulnerability** to open a private advisory draft.
3. Describe the issue, how to reproduce it, and its likely impact. A suggested fix is welcome.

Please do not open a public issue or discuss the problem in public until a fix has been released.

## What to Expect

Engram is maintained by a small team on a best-effort basis, so there is no guaranteed response time. We will acknowledge the report in the advisory thread, work on the fix there with you, and credit you in the release notes unless you ask us not to.
