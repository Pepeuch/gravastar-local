#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "site" / "original" / "hub.gravastar.com"
DEFAULT_OUTPUT = REPO_ROOT / "site" / "patched" / "hub.gravastar.com"
DEFAULT_VENDOR_SCRIPT = REPO_ROOT / "vendor" / "tdesign-icons-0.3.1.js"
DEFAULT_OFFLINE_VIDEO = REPO_ROOT / "patches" / "offline-video.html"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a patched local GravaStar mirror from the original static bundles.",
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--vendor-script", type=Path, default=DEFAULT_VENDOR_SCRIPT)
    parser.add_argument(
        "--offline-video-template",
        type=Path,
        default=DEFAULT_OFFLINE_VIDEO,
    )
    return parser.parse_args()


def require_path(path: Path, description: str) -> None:
    if not path.exists():
        raise SystemExit(f"{description} not found: {path}")


def copy_source_tree(source: Path, output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(source, output)


def patch_text_file(
    path: Path,
    replacements: list[tuple[str, str, str]],
) -> None:
    text = path.read_text(encoding="utf-8")

    for old, new, label in replacements:
        occurrences = text.count(old)
        if occurrences != 1:
            raise SystemExit(
                f"Expected exactly one occurrence for {label!r} in {path}, found {occurrences}.",
            )
        text = text.replace(old, new, 1)

    path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()

    require_path(args.source, "Original site root")
    require_path(args.vendor_script, "Vendored TDesign icon script")
    require_path(args.offline_video_template, "Offline video placeholder")

    copy_source_tree(args.source, args.output)

    connect_bundle = args.output / "gravastar" / "assets" / "index-CDT0qaCJ.js"
    icon_bundle = args.output / "gravastar" / "assets" / "index-Dg79dqpP.js"
    asset_dir = args.output / "gravastar" / "assets"

    require_path(connect_bundle, "Connect bundle")
    require_path(icon_bundle, "Icon bundle")

    patch_text_file(
        connect_bundle,
        [
            (
                "https://controlhub.top/gravastar/",
                "/gravastar/assets/offline-video.html#mouse",
                "offline mouse route placeholder",
            ),
            (
                "https://demo.hubx.pro/keyboard/?brand=grava-star",
                "/gravastar/v2/device",
                "local Beiying route",
            ),
            (
                "{vendorId:14126,productId:4204}",
                "{vendorId:14126,productId:4204},{vendorId:14126,productId:4325}",
                "K98 Pro PID 4325 filter",
            ),
            (
                "[4675,4204].includes(a)",
                "[4675,4204,4325].includes(a)",
                "K98 Pro PID 4325 family detection",
            ),
            (
                "//player.bilibili.com/player.html?bvid=BV1fdjEzyEZi&page=1&autoplay=0",
                "/gravastar/assets/offline-video.html#bilibili",
                "offline bilibili placeholder",
            ),
            (
                "https://www.youtube.com/embed/SL04XauQ3Ws?si=MViT6kRZuhXiDZ7A",
                "/gravastar/assets/offline-video.html#youtube",
                "offline youtube placeholder",
            ),
        ],
    )

    patch_text_file(
        icon_bundle,
        [
            (
                "https://tdesign.gtimg.com/icon/0.3.1/fonts/index.js",
                "/gravastar/assets/tdesign-icons-0.3.1.js",
                "local TDesign icon script",
            ),
        ],
    )

    shutil.copy2(args.vendor_script, asset_dir / "tdesign-icons-0.3.1.js")
    shutil.copy2(args.offline_video_template, asset_dir / "offline-video.html")

    patched_connect_text = connect_bundle.read_text(encoding="utf-8")
    patched_icon_text = icon_bundle.read_text(encoding="utf-8")

    for forbidden, label in [
        ("https://controlhub.top/gravastar/", "remote mouse route"),
        ("https://demo.hubx.pro/keyboard/?brand=grava-star", "remote Beiying route"),
        ("//player.bilibili.com/player.html?bvid=BV1fdjEzyEZi&page=1&autoplay=0", "remote bilibili embed"),
        ("https://www.youtube.com/embed/SL04XauQ3Ws?si=MViT6kRZuhXiDZ7A", "remote youtube embed"),
    ]:
        if forbidden in patched_connect_text:
            raise SystemExit(f"Patch verification failed: {label} is still present.")

    if "https://tdesign.gtimg.com/icon/0.3.1/fonts/index.js" in patched_icon_text:
        raise SystemExit("Patch verification failed: remote TDesign icon script is still present.")

    print(f"Patched site generated in: {args.output}")


if __name__ == "__main__":
    main()
