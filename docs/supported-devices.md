# Supported devices

## Documented identifiers

| Role | Decimal | Hex |
| --- | ---: | ---: |
| Vendor ID | 14126 | `0x372e` |
| Official known Product ID | 4204 | `0x106c` |
| Additional Product ID accepted by the local patch | 4325 | `0x10e5` |

## Notes

- The original connect bundle already knew the `14126/4204` device family.
- The local patch extends the same family detection to `14126/4325`.
- The patched mirror keeps the same frontend logic and only adjusts bundle routing and WebHID filters.
- A legacy `Beiying` family identifier `14139/4675` remains present in the upstream connect logic and is routed locally by the patched build.
