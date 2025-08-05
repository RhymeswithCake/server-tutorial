import asyncio
import websockets

async def hello():
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from the client!")

asyncio.run(hello())