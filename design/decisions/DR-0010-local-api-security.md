---
title: "Grid Network — Local API caller authentication"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-10
severity: Med
blocks: V1.1
linked_finding: H4/H7
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Local API caller authentication"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-10
severity: Med
blocks: V1.1
linked_finding: H4/H7
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-10 — Local API caller authentication

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-10
- Title: Local API caller authentication
- Severity: Med
- Blocks: V1.1
- Linked finding: [REVIEW-2026-10-11 H4/H7](../REVIEW-2026-10-11.md) (see section H4/H7 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-10: LOCAL API CALLER AUTHENTICATION AND KEY CUSTODY
[HIGH PRIORITY, IMPACTS EMBEDDED DEPLOYMENT AND MOBILE]

Problem:
v0.6.2 defines the local API (§17) but does not say which local processes may
call it, how callers are authenticated, or where private keys are stored. The
agent is called a "security boundary," but the boundary is not defined. This
is critical on mobile and embedded systems where the agent is often inside the
application process (H4).

Option A: OS-level caller identification + registered scopes [PROPOSED in §17]

  Transport: Unix domain socket (Linux/macOS), named pipe with ACL (Windows),
  embedded API with signature checks (iOS/Android).

  Caller ID: OS-provided peer credentials (SO_PEERCRED / getpeereid /
  named-pipe identity); mapped to a registered local client.

  Scopes:
    read ........ discover, resolve, authorize, status
    connect .... connect (service linkage only; no key access)
    admin ...... revoke, grant, pair

  Registration: each app is registered once with user approval; default
  (integrated apps) is read + connect. admin requires interactive confirmation
  or admin CLI.

  Key custody: private keys in OS keystore / TPM / Secure Enclave / StrongBox.
  Identity Root never crosses the API; it is offline or hardware-backed.

  Pros:
    - Clear boundaries: each app knows its authority.
    - Fails closed: unknown callers are rejected.
    - Mobile-friendly: platform native keystores.
    - Audit-friendly: every admin call is logged.

  Cons:
    - Implementation is platform-specific (socket on Linux, pipes on Windows,
      etc.).
    - Registration adds user friction on first app install.
    - Requires users to understand scopes (UX work).

Option B: TCP localhost + token authentication [SIMPLER, LESS SECURE]

  API listens on 127.0.0.1:port. Callers present a pre-shared token (stored
  in a config file or environment).

  Pros:
    - Single implementation for all platforms.
    - Simpler to debug (standard HTTP tools work).

  Cons:
    - Token-in-config is a credential-storage anti-pattern.
    - Any process on the machine can read the config file and call the API.
    - No caller identification; no per-app scoping.
    - On multi-user systems, a user with local access can impersonate any app.

Option C: Embedded only; no local IPC

  The agent is compiled into each application. No separate agent process.
  Applications call the agent as a library; no IPC boundary.

  Pros:
    - No IPC attack surface.
    - Simpler deployment (no extra binary).

  Cons:
    - Each app embeds the agent; key management varies per app.
    - No shared identity/relationship state across apps.
    - Contradicts the design goal ("consume a common local agent").
    - Mobile and desktop diverge significantly.

Recommendation:
Accept Option A (OS-level caller ID + scopes + secure keystores). Implement
platform-native security (socket/pipe/embedded API). Define the scope model
clearly in CONTRIBUTING.md and the agent documentation.

Consequences:
  - §17: update local API security model (as proposed).
  - Implementer guide: platform-specific socket/pipe creation, SCM_RIGHTS
    (Linux), named-pipe ACLs (Windows), iOS/Android framework integration.
  - Test vectors: unauthorized caller rejection, scope enforcement.
  - UX: user approval flow for registration; admin-scope confirmation.
  - Audit: log format for admin calls (caller, method, timestamp, parameters
    excluding secrets).

================================================================================
