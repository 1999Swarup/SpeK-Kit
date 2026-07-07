---
id: TL-ses
type: Tool
title: Amazon SES
description: AWS transactional email service.
status: proposed
category: email
maturity: stable
cost: usage-based
license: proprietary
confidence: high
tags: [infra, email]
created: 2026-07-06
updated: 2026-07-06
provides: [CAP-email]
alternative_to: [TL-sendgrid]
---

# Amazon SES

## What it does
Sends transactional email at low per-message cost within AWS.

## Known pitfalls
Sandbox mode requires domain verification before production sending.
