# Reverse-engineering notes

## Source of truth

- `site/original/hub.gravastar.com/gravastar/` is the preserved upstream static mirror.
- The repository does not hand-edit minified frontend bundles in place.
- The generated local build comes from `patches/apply_patches.py`.

## K98 Pro PID patch

The original connect bundle only exposed:

- `VID 14126 / PID 4204` in the WebHID filter list
- `VID 14126 / PID 4204` in the `Beiying` family detection branch

The local patch reproduces the manual change by:

- adding `PID 4325` to the connect-page WebHID filters
- adding `PID 4325` to the `Beiying` family detection branch

## Offline hardening

The original mirror still contained a few automatic remote loads:

- the TDesign icon font script hosted on `tdesign.gtimg.com`
- tutorial video iframes for Bilibili and YouTube
- a remote demo route for the `Beiying` family

The local patch replaces those automatic loads with local equivalents or local routing, while leaving explicit outbound help and social links untouched.
