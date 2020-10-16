from __future__ import annotations
from typing import *

import asyncio
import sys


async def handle_connection(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    while message := await reader.read(100):
        text = message.decode()
        print(f"Received {text!r} from {addr!r}")
        print(f"Sending {text!r}")
        writer.write(message)
        await writer.drain()
        if text == "quit\n":
            break
    print("Closing the connection")
    writer.close()

async def main() -> None:
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8888)
    addr = server.sockets[0].getsockname() if server.sockets else "unknown"
    print(f"Serving on {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
