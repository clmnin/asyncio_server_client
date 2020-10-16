from __future__ import annotations
from typing import *

import asyncio
import sys


async def send_file(file: IO[str]) -> None:
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    for message in file:
        # simulate network slowness
        print("Sending bytes: ", end="")
        for ch in message.encode():
            await asyncio.sleep(0.1)
            writer.write(bytes([ch]))
            print(f"{hex(ch)[2:].upper():0>2}", end="")
            sys.stdout.flush()
            if ch == 10:
                print()
        data = await reader.read(100)
        text = data.decode()
        print(f"Received {text!r}")
        if text == "quit":
            break

    print("Closing the connection")
    writer.close()

if __name__ == "__main__":
    asyncio.run(send_file(sys.stdin))
