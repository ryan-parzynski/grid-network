NOTICE — Heavy AI Agent usage in the creation of this project

Grid Network is a design for portable identity and authorization between devices.
Every self-hosted application eventually needs remote access. Today that access either depends on a vendor (commercial mesh VPNs), requires an expert (self-hosted VPNs), or exposes the user to risk (port forwarding). The structural reason is that coordination has always required somebody to be the authority. Authorities cost money to operate, so somebody has to pay.

Grid Network is the first design that solves coordination without introducing an authority. Identity is a keypair, not an account. Authorization is local, not remote. Discovery is signed, not centralized. Infrastructure is replaceable, not mandatory.

The result is a protocol that costs nothing to operate, requires nobody's permission, and cannot be captured by any single entity. It is designed to be for private connectivity what Linux is for operating systems and TLS is for transport security.

This repository contains the complete design specification (v0.6.2, frozen) and supporting rationale. It does not yet contain an implementation. The design is published for review, discussion, and adoption.

Status: Design phase complete. Reference implementation not yet started.

If you are:
    An application developer — read docs/RATIONALE.md Part IV.
    A self-hoster — read the summary in README.
    A skeptic — read docs/DESIGN-DEFENSE.md.
    A protocol implementer — read docs/PROTOCOL.md.
