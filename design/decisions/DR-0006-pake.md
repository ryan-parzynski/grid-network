---
title: "Grid Network — PAKE algorithm and transcript"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-06
severity: High
blocks: V1
linked_finding: C2/C6
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — PAKE algorithm and transcript"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-06
severity: High
blocks: V1
linked_finding: C2/C6
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-06 — PAKE algorithm and transcript

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-06
- Title: PAKE algorithm and transcript
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 C2/C6](../REVIEW-2026-10-11.md) (see section C2/C6 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-06: PAIRING ALGORITHM AND TRANSCRIPT CONTRACT
[BLOCKING, CRITICAL PRIORITY]

Problem:
C6 and the spec identify SPAKE2 or CPace as candidates, but neither is fully
specified. The protocol's security rests on the pairing transcript (§10);
implementations must agree byte-for-byte. Without test vectors and an exact
algorithm choice, interoperability cannot be claimed.

Option A: SPAKE2 with specified transcript format [PROPOSED in §10]

  Algorithm: SPAKE2 (https://datatracker.ietf.org/doc/html/rfc9383).
  Transcript binding: SHA-256 over a canonical CBOR array:
    ["grid/pairing/v1", protocol_version, context_label, peer_id_A,
     peer_id_B, identity_root_A, identity_root_B, ephemeral_msg_A,
     ephemeral_msg_B, code_session_id]

  All serialized in canonical CBOR per §13.1.
  relationship_id derived from SHA-256(pake_transcript_hash), per M1.

  Pros:
    - RFC 9383 is stable and well-reviewed.
    - Clear threat model (short code, PAKE security).
    - Moderate complexity; multiple implementations exist.

  Cons:
    - The RFC leaves transcript/context binding to the application; we must
      specify it fully (done above, but adds work).
    - Slightly slower than CPace for very long codes.

Option B: CPace (https://datatracker.ietf.org/doc/html/rfc9383 Appendix A)

  Algorithm: CPace.
  Transcript: same CBOR structure as Option A.

  Pros:
    - More efficient for very long code strings.
    - Equally secure.

  Cons:
    - Less mature than SPAKE2; fewer reference implementations.
    - Security analysis is more recent; larger field for hidden bugs.
    - RFC is an appendix; less standalone clarity.

Recommendation:
Accept Option A (SPAKE2). Stability and maturity outweigh CPace's efficiency
gain. Write the exact transcript binding in a PAKE specification document
(not in the core protocol document; PAKE is a bounded, self-contained choice).

Consequences:
  - New document: spec/PAIRING.md, specifying SPAKE2, transcript, code
    lifetimes, retry limits, verification value (SAS) derivation, test vectors.
  - Update §10 with a reference to PAIRING.md and the minimum output contract.
  - Reference verifier: SPAKE2 library integration (libspake2 or eq.).
  - Test vectors: successful pairings, failed codes, timeouts, SAS
    verification.
  - D-07 (relationship privacy) depends on pairing completing the
    relationship_id derivation.

================================================================================
