# Grid Network — Parameters

**Revision:** 2.1
**Protocol version:** v0.6.2

This document defines every symbol used in a normative rule. Literal
values do not appear in normative text; the rule names a symbol and
this table gives the default. A conformant implementation may choose
different values for parameters marked "policy"; it must not choose
different values for parameters marked "protocol".

---

## Protocol parameters

These values are fixed by the protocol. An implementation that uses a
different value is non-conformant.

| Symbol | Value | Meaning | Defined in |
|---|---|---|---|
| `ED25519_SIGNATURE_BYTES` | 64 | Length of an Ed25519 signature | Protocol §43 |
| `ED25519_PUBLIC_KEY_BYTES` | 32 | Length of an Ed25519 public key | Protocol §43 |
| `SHA256_HASH_BYTES` | 32 | Length of a SHA-256 hash | `OBJECTS.md §2` |
| `MAX_SEQUENCE_NUMBER` | 2^64 − 1 | Largest valid `sequence` value | `OBJECTS.md §2.2` |
| `MIN_SEQUENCE_NUMBER` | 1 | Smallest valid `sequence` value | `OBJECTS.md §2.2` |
| `CBOR_SMALL_INT_MAX` | 23 | Largest value using the direct additional-info encoding | `OBJECTS.md §2.2` |
| `MAX_INTEGER_VALUE` | 2^64 − 1 | Largest permitted integer in any CBOR value | `OBJECTS.md §2.2` |
| `CBOR_NULL_BYTE` | 0xf6 | The CBOR encoding of `null` | `OBJECTS.md §2.9` |
| `CBOR_FALSE_BYTE` | 0xf4 | The CBOR encoding of `false` | `OBJECTS.md §2.9` |
| `CBOR_TRUE_BYTE` | 0xf5 | The CBOR encoding of `true` | `OBJECTS.md §2.9` |
| `UNICODE_NFC_VERSION` | 15.0 | Unicode version used for text string normalization | `OBJECTS.md §2.4` |

## Protocol bounds

These values bound protocol-defined fields. They are fixed.

| Symbol | Value | Meaning | Defined in |
|---|---|---|---|
| `MAX_CAPABILITY_CONSTRAINTS` | 32 | Maximum entries in a grant's `constraints` map | Protocol §11 |
| `MAX_CONSTRAINT_VALUE_BYTES` | 1024 | Maximum byte length of a constraint value | Protocol §11 |
| `MAX_CAPABILITY_NAMESPACE_LENGTH` | 255 | Maximum length of a capability namespace | Protocol §11 |

## Pairing parameters

These values are policy defaults. An implementation may use different
values, but the defaults below are recommended.

| Symbol | Default | Meaning | Defined in |
|---|---|---|---|
| `PAIRING_VERIFICATION_CODE_DIGITS` | 6 | Digits in the human-verified code | Protocol §21.2 |
| `PAIRING_CODE_VALIDITY` | 600 seconds | Window during which a pairing code is valid | Protocol §21.2 |
| `PAIRING_PAKE_SECRET_BITS` | 128 | Entropy of the PAKE secret | Protocol §21.2 |
| `PAIRING_MAX_ATTEMPTS` | 5 | Failed PAKE attempts before the pairing session is invalidated | Protocol §21 |

## Time parameters

Policy defaults for time-based behavior. An implementation may tune
these.

| Symbol | Default | Meaning | Defined in |
|---|---|---|---|
| `MAX_CLOCK_SKEW` | 6 hours | Maximum acceptable difference between verifier clock and issuer clock for absolute timestamps | Protocol §39 (F3) |
| `MAX_LEASE_AGE` | 2 × lease nominal duration | Maximum age of a lease measured from its `issued_at` | Protocol §10 |
| `DEFAULT_REACHABILITY_TTL` | 1 hour | Default validity of a reachability record | Protocol §24 |
| `DEFAULT_REVOCATION_POLL_INTERVAL` | 30 minutes | Recommended interval between revocation polls | Protocol §31 |
| `DEFAULT_LEASE_DURATION_MEDIA` | 30 days | Illustrative default for media streaming | Protocol §10 |
| `DEFAULT_LEASE_DURATION_FILE` | 7 days | Illustrative default for file access | Protocol §10 |
| `DEFAULT_LEASE_DURATION_SSH` | 1 hour | Illustrative default for shell access | Protocol §10 |
| `DEFAULT_LEASE_DURATION_ADMIN_SSH` | 15 minutes | Illustrative default for administrative shell access | Protocol §10 |

## Relay parameters

Policy defaults for relay operation.

| Symbol | Default | Meaning | Defined in |
|---|---|---|---|
| `DEFAULT_FREE_TIER_LIMITS` | 1 Mbps concurrent, 10 GB/month | Fair-share caps for free tier | `commercial/MODEL.md` |
| `DEFAULT_FREE_RATE_LIMIT` | 10 lookups/sec | Rate limit for free tier rendezvous queries | `commercial/MODEL.md` |
| `DEFAULT_STANDARD_MIN_BPS` | 10 Mbps | Guaranteed minimum relay bandwidth for standard tier | `commercial/MODEL.md` |
| `DEFAULT_STANDARD_RATE_LIMIT` | 30 lookups/sec | Rate limit for standard tier | `commercial/MODEL.md` |
| `DEFAULT_PRIORITY_MIN_BPS` | 50 Mbps | Guaranteed minimum relay bandwidth for priority tier | `commercial/MODEL.md` |
| `DEFAULT_PRIORITY_SLA_LATENCY` | 100 ms | Latency bound for priority tier | `commercial/MODEL.md` |
| `DEFAULT_DEDICATED_SLA_UPTIME` | 99.99% | Uptime SLA for dedicated tier | `commercial/MODEL.md` |
| `DEFAULT_PRIORITY_SLA_UPTIME` | 99.5% | Uptime SLA for priority tier | `commercial/MODEL.md` |
| `DEFAULT_STANDARD_SLA_UPTIME` | 99% | Uptime SLA for standard tier | `commercial/MODEL.md` |

## Commercial parameters

Policy defaults for the commercial model. These are illustrative; the
protocol does not require any particular value.

| Symbol | Default | Meaning | Defined in |
|---|---|---|---|
| `CREDIT_TO_GB_RATIO` | 1 credit = 1 GB | Standard exchange rate | `operations/RELAYS.md` |
| `GEOGRAPHIC_MULTIPLIER_ABUNDANT` | 1 | Credit multiplier in regions with abundant relays | `operations/RELAYS.md` |
| `GEOGRAPHIC_MULTIPLIER_SCARCE` | 3 | Credit multiplier in scarce regions | `operations/RELAYS.md` |
| `GEOGRAPHIC_MULTIPLIER_VERY_SCARCE` | 5 | Credit multiplier in very scarce regions | `operations/RELAYS.md` |
| `DEFAULT_DEVELOPER_FUND_SHARE` | 20% | Fraction of relay revenue contributed to developer funding | `commercial/MODEL.md` |
| `DEFAULT_REACHABILITY_CREDIT_REWARD` | 1 credit/day | Credit earned per day of reachability published | TODO: no document defines this parameter |

## Conformance targets

Policy targets for milestone completion. These are not requirements on
implementations; they are project goals.

| Symbol | Target | Meaning |
|---|---|---|
| `TARGET_DIRECT_CONNECTION_RATE` | 70% | Fraction of deployments achieving direct connection without relay |
| `TARGET_CONNECTION_SUCCESS_RATE` | 80% | Fraction of attempted connections that succeed on first attempt |
| `TARGET_MOBILE_BATTERY_USE` | 5% per day | Maximum battery draw of a mobile agent |

## Adding a parameter

A new parameter requires:

1. A symbol name, uppercase, underscore-separated.
2. A category — protocol, bounds, pairing, time, relay, commercial,
   conformance.
3. A default value and unit.
4. A reference to the section that uses it.

Parameters marked "protocol" require a protocol-version bump to
change. Parameters marked "policy" may be changed by an implementation
without a version bump, but the default in this table changes only on a
document revision.