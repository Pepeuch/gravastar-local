# Patch workflow

`patches/apply_patches.py` regenerates the local mirror from `site/original/` into `site/patched/`.

It currently performs four categories of deterministic bundle changes:

1. Add K98 Pro PID `4325` to the WebHID filters and family detection.
2. Route the `Beiying` family to the local `/gravastar/v2/device` page instead of the remote demo host.
3. Replace the automatic `mouse` route with a local offline placeholder instead of the remote host.
4. Replace automatic remote asset loads with local files:
   - TDesign icon script
   - Bilibili and YouTube tutorial embeds

The script is intentionally strict:

- it copies a fresh output tree each time;
- it expects each target string to appear exactly once;
- it exits with an error if an upstream bundle has changed and the patch is no longer safe.

Usage:

```bash
python3 patches/apply_patches.py
```
