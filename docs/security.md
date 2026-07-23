# Security notes

## Local-only serving

- The mirror is served by Nginx on `127.0.0.1:18088` by default.
- The published port can be overridden with `GRAVASTAR_PORT`.
- WebHID access remains between the browser and the locally attached device.
- The Docker/Nginx setup adds a restrictive CSP so the local page only executes local scripts and frames local content.

## Automatic remote loads removed

The patched build replaces the original automatic remote loads with local resources:

- `https://tdesign.gtimg.com/icon/0.3.1/fonts/index.js`
  becomes a vendored local file under `/gravastar/assets/tdesign-icons-0.3.1.js`
- the Bilibili and YouTube tutorial iframes are replaced by a local offline placeholder
- the `Beiying` demo route points to the local `/gravastar/v2/device`
- the original `mouse` route to `https://controlhub.top/gravastar/` now points to a local offline placeholder

## Remaining outbound links

The frontend still contains explicit outbound help, store and social links. They are only followed if the user clicks them; they are not loaded automatically by the mirrored site itself.

## Optional localhost music feature

The upstream bundles still contain code paths related to a local music companion and `localhost:15371`. This repository does not try to restore or validate that optional path. It remains documented as an optional local-only branch and is not required for core keyboard configuration.
