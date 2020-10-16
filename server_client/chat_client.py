from __future__ import annotations
from typing import *

import asyncio
import sys
import contextlib
import aiofiles

from chat_streams import split_lines, write


async def handle_reads(reader: asyncio.StreamReader) -> None:
    async for message in split_lines(reader):
        text = message.decode()
        print(f"Received {text!r}")
        if text == "quit\n" or text == "quit":
            break


async def send_file(file: IO[str]) -> None:
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    read_handler = asyncio.create_task(handle_reads(reader))
    loop = asyncio.get_event_loop()
    # previously we used a blocking for loop here, because of that
    # we had a blocking call that prevented read (which is an async task)
    async for message in aiofiles.threadpool.wrap(file, loop=loop):
        await write(writer, message.encode())
    read_handler.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await read_handler
    print("Closing the connection")
    writer.close()

if __name__ == "__main__":
    asyncio.run(send_file(sys.stdin))
