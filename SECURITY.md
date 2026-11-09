# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 4.x | Yes |
| 3.x | No |

## Reporting a vulnerability

Do not open a public issue for a security problem.

Email `sutantodadang@gmail.com` with:

- the affected file and version,
- a description of the issue,
- a minimal reproduction or proof of concept,
- the impact you believe it has.

You will receive an acknowledgement within 7 days. Please allow 90 days for a fix before public disclosure.

## Scope

This repository contains instructions and small scripts. It does not run as a service. Relevant reports include:

- a script that can delete or exfiltrate data when run as documented,
- instructions that would lead an agent to weaken authentication, authorization, or tenancy,
- a dependency or install step that executes untrusted code.
