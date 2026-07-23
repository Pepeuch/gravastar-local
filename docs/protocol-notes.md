# Protocol and platform notes

## Connect flow

The connect page uses `navigator.hid.requestDevice()` with a static filter list embedded in `assets/index-CDT0qaCJ.js`.

The local patch extends that filter list for:

- `VID 14126 / PID 4204`
- `VID 14126 / PID 4325`

The patched connect page then routes the detected device family to the local SPA route `/gravastar/v2/device`.

The only exception is the original `mouse` family branch: instead of opening the upstream remote configurator, the local mirror now sends that route to a local placeholder page so the offline build fails cleanly without attempting a network fetch.

## Linux WebHID

Requirements:

- recent Chromium, Chrome or Edge
- access from `localhost` or another trusted secure context
- a permissive enough `udev` rule for the matching HID/USB nodes

Example install:

```bash
sudo cp docs/99-gravastar-webhid.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger
```

Then unplug and reconnect the keyboard before reopening the browser.

## Browser support

- Chromium-based browsers: supported for WebHID
- Firefox: no practical support here
- Safari: no practical support here

## Optional localhost integration

The upstream code references a local companion channel on `localhost:15371` for music/rhythm features. That branch is optional and outside the scope of the current local mirror.
