from __future__ import annotations
from typing import *

import asyncio
import sys
from chat_streams import split_lines

async def handle_connection(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info("peername")
    async for message in split_lines(reader):
        text = message.decode()
        print(f"Received {text!r} from {addr!r}")
        print(f"Sending {text!r}")
        writer.write(message)
        await writer.drain()
        if text == "quit":
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
