# Versioning Policy

Grid Network follows semantic versioning for the protocol specification:

## Format: vMAJOR.MINOR.PATCH

- **v0.6.2** (current, frozen)
- **v0.7.0** (next: test vectors, cleanup)
- **v1.0.0** (stable, long-term support)

## Version Semantics

### PATCH (v0.6.2 → v0.6.3)
- Bug fixes only
- No new features
- No new object types
- No new fields in existing objects
- Backward compatible
- Change process: Maintainer review only

### MINOR (v0.6.2 → v0.7.0)
- New features allowed
- New object types allowed
- New optional fields in objects
- Backward compatible (old objects understood by new implementations)
- Change process: RFC + 14-day discussion + maintainer decision

### MAJOR (v0.6.2 → v1.0.0)
- Breaking changes allowed
- Incompatible changes
- Removal of deprecated features
- Backward compatible: NO
- Change process: RFC + 30-day discussion + consensus required

## Document Versioning

Each document has its own independent version:
- spec/PROTOCOL.md v0.6.2
- spec/OBJECTS.md v0.2
- design/RATIONALE.md v2.0
- commercial/MODEL.md v6.0
- design/LINEAGE.md v1.0

When PROTOCOL.md increments MINOR, dependent docs increment MINOR.
When PROTOCOL.md increments MAJOR, all docs increment MAJOR.

## Support Timeline

- v0.x: Maintained until v1.0.0 ships + 5 years
- v1.x: Maintained for 5 years minimum
- End of support ≠ protocol stops working (implementations can run indefinitely)
