import asyncio
import websockets

from detector import run_detection

async def main():
    async with websockets.serve(run_detection, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    print("Starting WebSocket server...")
    asyncio.run(main())
    print("WebSocket server stopped.")
