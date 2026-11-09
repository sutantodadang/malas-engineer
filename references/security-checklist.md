# Security checklist

Read this before touching authentication, authorization, tenancy, payments, file upload, or an external integration.

## Review method

1. Map the changed trust boundaries.
2. Identify the assets: credentials, personal data, money, tenant data, admin actions.
3. For each entry point, ask who can call it and what they can reach.
4. Follow the data to storage, logs, and outbound calls.
5. Check failure behavior. Failures must fail closed.

## Authentication

- [ ] Credentials, tokens, and session identifiers are generated with a cryptographically secure source.
- [ ] Tokens are validated for issuer, audience, signature, expiry, and not-before.
- [ ] Unsigned or wrongly signed tokens are rejected. Unexpected algorithms are rejected.
- [ ] Expired and revoked credentials stop working within the expected window.
- [ ] Session identifiers are invalidated on logout and privilege change.
- [ ] Sensitive actions require re-authentication or MFA where appropriate.
- [ ] Service-to-service identities are scoped and not shared across environments.

## Authorization

- [ ] Every new route, query, and object access is checked on the server.
- [ ] Object-level authorization: changing an identifier does not expose another user's object.
- [ ] Function-level authorization: lower-privilege roles cannot reach privileged actions.
- [ ] Authorization is enforced centrally or by a consistent pattern, not by scattered ad hoc checks.
- [ ] Deny by default. New endpoints are private until explicitly opened.
- [ ] The front end is not the enforcement point.

## Tenancy

- [ ] Every query, including background jobs, exports, reports, and webhooks, applies tenant scope.
- [ ] A token for tenant A cannot read or modify tenant B data, even with a known identifier.
- [ ] List endpoints, search, and aggregates cannot leak cross-tenant counts or rows.
- [ ] Cache keys and queue messages carry tenant identity.
- [ ] Tests cover cross-tenant access attempts.

## Input and output

- [ ] All external input is validated at the boundary: type, length, range, format, encoding.
- [ ] Queries are parameterized. No string concatenation of SQL.
- [ ] File paths, URLs, redirects, and deserialized data are constrained.
- [ ] Output is encoded for its context: HTML, JSON, shell, SQL, URL.
- [ ] Mass assignment is blocked. Only allowed fields bind to models.
- [ ] Uploads are type-checked, size-limited, and stored outside the web root.

## Cryptography

- [ ] Vetted libraries and current algorithms are used.
- [ ] Keys come from a key manager, not source code.
- [ ] Randomness is cryptographically secure where it matters.
- [ ] Password hashing uses a memory-hard algorithm with a current cost factor.
- [ ] Encryption includes integrity protection where required.

## Secrets and data

- [ ] No secrets, tokens, or personal data in code, logs, error messages, or analytics.
- [ ] Secrets are injected at runtime from a secret manager.
- [ ] Secrets can be rotated without redeploying every service.
- [ ] Development, test, and production secrets are separate.
- [ ] Personal data is minimized, masked where possible, and retained only as long as needed.

## Errors and logging

- [ ] Failures fail closed.
- [ ] Clients receive generic errors, not stack traces or internal identifiers.
- [ ] Security events are logged: auth success and failure, authorization failure, token issuance and revocation, privilege change, rate-limit trigger.
- [ ] Logs carry a correlation identifier and exclude sensitive content.
- [ ] Alerts exist for repeated authorization failures and enumeration patterns.

## Abuse and availability

- [ ] Rate limits exist on authentication, recovery, OTP, and expensive endpoints.
- [ ] Limits apply per user, per IP, and per tenant where appropriate.
- [ ] Enumeration resistance: responses do not reveal whether an account or object exists.
- [ ] Quotas are enforced before expensive work starts.
- [ ] Timeouts, body size limits, and queue caps are set.

## Dependencies and supply chain

- [ ] Each new dependency is necessary, maintained, and the intended package.
- [ ] Versions are pinned and lockfiles are committed.
- [ ] Dependency audit (SCA) runs in CI.
- [ ] SAST runs in CI or before merge.
- [ ] Secret scanning runs on commits and pull requests.
- [ ] Build artifacts have provenance. SLSA or an equivalent level is chosen deliberately.
- [ ] CI tokens and deploy credentials follow least privilege.
- [ ] Third-party webhooks are authenticated and replay-resistant.
- [ ] OAuth scopes are the narrowest that work.

## Threat modeling

Use STRIDE for new surfaces or significant changes:

| Threat | Question |
|---|---|
| Spoofing | Can an attacker impersonate a user or service? |
| Tampering | Can data or requests be modified in transit or at rest? |
| Repudiation | Can an action be denied without evidence? |
| Information disclosure | Can data leak through responses, logs, or timing? |
| Denial of service | Can one caller exhaust a shared resource? |
| Elevation of privilege | Can a lower role reach a higher action? |

## References

- OWASP Secure Code Review Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- SLSA: https://slsa.dev/
