# Applications

Application integrations for Grid Network.

## Files

- `README.md` — This file.

## Reading Order

1. Integration guide (to be created).
2. Example integrations (to be created).

## Current Status

Application integrations begin in Phase 10+. See `../ROADMAP.md`.

Target applications for integration:
- Immich (photo management)
- Jellyfin (media streaming)
- Nextcloud (file sync/sharing)
- Home Assistant (home automation)
- Syncthing (file synchronization)
- Paperless (document management)
- PhotoPrism (photo management)
- Vaultwarden (password management)
- Gitea (code hosting)
- And others

## Integration Pattern

Applications integrate with the local Grid agent via a small API:

```
grid.connect(service_link_id, capability) → local connection handle
grid.resolve(peer_id)                     → peer state
grid.discover()                            → list of known peers
grid.revoke(object_id)                     → issue revocation
grid.status()                              → daemon state
```

The application calls `grid.connect` with the service it wants to reach and the capability it wants to exercise. The agent returns a local URL. The application treats that URL like any other local service.
