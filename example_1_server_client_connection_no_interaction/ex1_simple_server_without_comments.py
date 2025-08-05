import asyncio
import websockets

async def handle_client(websocket):
    print("Client connected")

    message = await websocket.recv()
    print("Received from client:", message)

    print("Done.")

async def main():
    async with websockets.serve(handle_client, "localhost", 12345):
        print("Server is running on ws://localhost:12345")
        await asyncio.Future() # Run this forever. Ctrl-C breaks this

asyncio.run(main())
