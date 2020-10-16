from __future__ import annotations
from typing import *

import asyncio


async def split_lines(reader: asyncio.StreamReader) -> AsyncIterator[bytes]:
    data = b""
    try:
        while data := data + await reader.read(100):
            if b'\n' in data:
                message, data = data.split(b"\n", 1)
                yield message
    except ConnectionResetError:
        pass
    if data:
        yield data
