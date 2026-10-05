**NOTICE — Heavy AI Agent usage in the creation of this project**

Grid Network is a design for portable identity and authorization between devices.

Every self-hosted application eventually needs remote access. Today the choices are to expose it to the internet, depend on a vendor, or become a sysadmin. Grid Network is a protocol that provides a fourth option: identity and authorization that belong to the user, that survive infrastructure changes, and that any application can depend on.

The reason private connectivity isn't free today is not technical — it's structural. Every current approach either charges money (commercial mesh VPNs), requires an expert (self-hosted VPNs), or exposes the user to risk (port forwarding). The structural reason is that coordination requires somebody to be the authority, and authorities cost money to operate, so somebody has to pay. If coordination can be decentralized without introducing a new authority, the cost structure changes.

This repository contains the complete design specification (v0.6.2, frozen) and supporting rationale. It does not yet contain an implementation. The design is published for review, discussion, and adoption.

**Status:** Design phase complete. Reference implementation not yet started.

**If you are:**
- An application developer — read `docs/RATIONALE.md` Part IV.
- A self-hoster — read the summary in `README`.
- A skeptic — read `docs/DESIGN-DEFENSE.md`.
- A protocol implementer — read `docs/PROTOCOL.md`.
