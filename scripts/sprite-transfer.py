#!/usr/bin/env python3
"""Transfer files between Sprite environments using the FS API."""

import argparse
import subprocess
import sys
import urllib.parse


def api_call(sprite: str, method: str, path: str, data: bytes = None) -> subprocess.CompletedProcess:
    """Make an API call to a sprite."""
    cmd = ["sprite", "api", "-s", sprite, path]
    if method != "GET":
        cmd.extend(["-X", method])
    if data is not None:
        cmd.extend(["--data-binary", "@-"])

    return subprocess.run(
        cmd,
        input=data,
        capture_output=True,
    )


def read_file(sprite: str, path: str) -> bytes:
    """Read a file from a sprite."""
    encoded_path = urllib.parse.quote(path, safe="")
    result = api_call(sprite, "GET", f"/fs/read?path={encoded_path}")
    if result.returncode != 0:
        print(f"Error reading from {sprite}:{path}", file=sys.stderr)
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    return result.stdout


def write_file(sprite: str, path: str, data: bytes, mkdir: bool = True) -> None:
    """Write a file to a sprite."""
    encoded_path = urllib.parse.quote(path, safe="")
    query = f"/fs/write?path={encoded_path}"
    if mkdir:
        query += "&mkdir=true"

    result = api_call(sprite, "PUT", query, data)
    if result.returncode != 0:
        print(f"Error writing to {sprite}:{path}", file=sys.stderr)
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def parse_location(loc: str) -> tuple[str | None, str]:
    """Parse 'sprite:path' or just 'path' into (sprite, path)."""
    if ":" in loc and not loc.startswith("/"):
        sprite, path = loc.split(":", 1)
        return sprite, path
    return None, loc


def main():
    parser = argparse.ArgumentParser(
        description="Transfer files between Sprite environments",
        epilog="""
Examples:
  %(prog)s my-sprite:/app/config.json ./config.json
  %(prog)s ./local-file.txt other-sprite:/tmp/file.txt
  %(prog)s sprite-a:/data/file sprite-b:/data/file
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", help="Source: sprite:path or local path")
    parser.add_argument("dest", help="Destination: sprite:path or local path")

    args = parser.parse_args()

    src_sprite, src_path = parse_location(args.source)
    dst_sprite, dst_path = parse_location(args.dest)

    if src_sprite is None and dst_sprite is None:
        print("Error: At least one location must be a sprite (sprite:path)", file=sys.stderr)
        sys.exit(1)

    # Read source
    if src_sprite:
        print(f"Reading from {src_sprite}:{src_path}...", file=sys.stderr)
        data = read_file(src_sprite, src_path)
    else:
        with open(src_path, "rb") as f:
            data = f.read()

    # Write destination
    if dst_sprite:
        print(f"Writing to {dst_sprite}:{dst_path}...", file=sys.stderr)
        write_file(dst_sprite, dst_path, data)
    else:
        with open(dst_path, "wb") as f:
            f.write(data)

    print(f"Transferred {len(data)} bytes", file=sys.stderr)


if __name__ == "__main__":
    main()
