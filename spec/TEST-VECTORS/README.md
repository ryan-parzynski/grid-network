# Test Vectors

Byte-exact normative test vectors for Grid Network v0.6.2.

## Structure

```
v0.6.2/
├── README.md              # This file
├── positive/              # Valid objects that MUST be accepted
│   ├── identity-document/
│   ├── device-binding/
│   ├── service-binding/
│   ├── key-binding/
│   ├── key-revocation/
│   ├── relationship-assertion/
│   ├── relationship-termination/
│   ├── rendezvous-manifest/
│   ├── operator-manifest/
│   ├── grant/
│   ├── lease/
│   ├── grant-revocation/
│   ├── lease-revocation/
│   ├── service-record/
│   ├── reachability-record/
│   ├── stream-resolution/
│   ├── identity-continuity/
│   ├── relay-ticket/
│   └── relay-node-record/
├── negative/              # Invalid objects that MUST be rejected
│   ├── identity-document/
│   ├── device-binding/
│   └── ... (one per object type, 3+ variants each)
└── conformance-scenarios/ # Full protocol scenarios from PROTOCOL.md §61
    └── ... (17 scenarios)
```

## Vector Format

Each test vector is a JSON file with:

```json
{
  "name": "identity-document-seq1-basic",
  "version": "0.6.2",
  "type": "positive",
  "description": "Minimal identity document, sequence 1, no relationships",
  "input": { ... },
  "canonical_cbor": "a1...",
  "expected_hashes": {
    "payload_id": "sha256:abcd1234...",
    "object_id": "sha256:xyz789...",
    "chain_hash": "sha256:chain_hash_value..."
  },
  "expected_signature": "ed25519:sig_value...",
  "verification_steps": [
    "Parse CBOR",
    "Verify domain separator",
    "Recompute payload_id",
    "Recompute chain_hash",
    "Verify Ed25519 signature",
    "Accept object"
  ],
  "spec_reference": "PROTOCOL.md §7.8, OBJECTS.md §6"
}
```

Negative test vectors include `modification`, `expected_rejection`, and `expected_rejection_reason` fields.

## Production Status

Test vectors are **not yet created**. See OBJECTS.md §11 for the production sequence (53+ vectors planned across 7 phases).
