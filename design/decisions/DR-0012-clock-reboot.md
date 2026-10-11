---
title: "Grid Network — Monotonic clock reset on reboot"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-12
severity: Med
blocks: V1.1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Monotonic clock reset on reboot"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-12
severity: Med
blocks: V1.1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-12 — Monotonic clock reset on reboot

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-12
- Title: Monotonic clock reset on reboot
- Severity: Med
- Blocks: V1.1
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md) (see section — or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-12: MONOTONIC CLOCK RESET ON REBOOT AND RELATIVE VALIDITY
[HIGH PRIORITY, OPERATIONAL IMPACT]

Problem:
v0.6.2 forbids falling back to wall-clock time after a monotonic clock reset
(reboot). Every relative-validity lease becomes unverifiable and the device
fails closed until refresh. This will feel like an outage to users, but the
spec does not acknowledge it or provide a graceful recovery path (H6).

Option A: Persisted wall-clock lower bound [PROPOSED in §12]

  On shutdown (and periodically, ~60 s), persist (wall_clock_now,
  accumulated_elapsed) for each relative-validity object.

  On boot:
    - If wall clock >= persisted value: relative validity is
      persisted_elapsed + (wall_now − persisted_wall), never less than
      persisted_elapsed. Clock did not go backwards.
    - If wall clock < persisted value: device remains STALE until refresh or
      clock is corrected. Never count time as unelapsed.

  Pros:
    - Survives reboots without hard failure.
    - Still fails closed if the clock actually goes backwards (security
      property retained).
    - Incremental: does not change the validity check, only the startup logic.
    - User-visible improvement: users won't notice brief access pause after
      reboot if they refresh within seconds.

  Cons:
    - Adds persistent state (one more data structure).
    - Requires periodic checkpointing (implementation detail).
    - If the device's filesystem is corrupted/reset, the persisted state is
      lost and the device falls back to STALE-on-boot.

Option B: Wall clock allowed; trust device's clock

  Remove the monotonic-clock requirement. Use wall clock for all relative
  validity. If the clock goes backwards or the device reboots, relative
  validity is recomputed from wall clock.

  Pros:
    - Simpler: no checkpoint logic.
    - No STALE-on-boot experience.

  Cons:
    - Loses monotonic-clock protection against clock-skew attacks.
    - A compromised device that resets its clock can extend expired leases.
    - Violates the "fail closed on clock skew" principle.

Option C: No recovery; accept the STALE-on-boot experience

  Relative validity is still lost on reboot. Devices must refresh. Users
  are told in documentation that "access may pause briefly after restart."

  Pros:
    - Simplest: no code change.

  Cons:
    - Poor user experience.
    - Conflict with deployment reality: home servers, mobile, laptops all
      reboot.

Recommendation:
Accept Option A (persisted wall-clock lower bound). Balances security and
operational realism. Document the behavior in user guides.

Consequences:
  - §12: update reboot rule (as proposed).
  - Implementer guide: checkpoint timing, persistence format, clock-skew
    handling.
  - Test vectors: reboot scenarios (clock forward, clock backward, no
    persisted state).
  - User docs: explain the behavior ("brief pause after restart is expected").
  - D-12 enables reasonable relative-validity operation without sacrificing
    monotonic-time protection.

================================================================================
