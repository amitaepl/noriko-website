# -*- coding: utf-8 -*-
"""
Read pixel dimensions from PNG / JPEG / WebP headers.

Pillow is not installed and the site has no dependencies, so this parses the
few bytes needed. Every <img> on the site carries width and height to prevent
layout shift, so the build needs this for any image dropped into the project.
"""
import struct


def _png(f):
    f.seek(16)
    return struct.unpack(">II", f.read(8))


def _jpeg(f):
    f.seek(2)
    while True:
        b = f.read(1)
        if not b:
            return None
        if b != b"\xff":
            continue
        marker = f.read(1)
        while marker == b"\xff":
            marker = f.read(1)
        m = marker[0]
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            continue
        seg = f.read(2)
        if len(seg) < 2:
            return None
        length = struct.unpack(">H", seg)[0]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            data = f.read(5)
            h, w = struct.unpack(">HH", data[1:5])
            return w, h
        f.seek(length - 2, 1)


def _webp(f):
    f.seek(12)
    chunk = f.read(4)
    if chunk == b"VP8 ":
        f.seek(26)
        w, h = struct.unpack("<HH", f.read(4))
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        f.seek(21)
        b = f.read(4)
        n = struct.unpack("<I", b)[0]
        return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
    if chunk == b"VP8X":
        f.seek(24)
        d = f.read(6)
        w = d[0] | (d[1] << 8) | (d[2] << 16)
        h = d[3] | (d[4] << 8) | (d[5] << 16)
        return w + 1, h + 1
    return None


def img_size(path):
    """(width, height), or None if the format is not recognised."""
    with open(path, "rb") as f:
        head = f.read(12)
        f.seek(0)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            return _png(f)
        if head.startswith(b"\xff\xd8"):
            return _jpeg(f)
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            return _webp(f)
    return None


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(p, img_size(p))
