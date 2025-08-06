# Example 3: chat_server

import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket):
    print(f"New client connected.")
    connected_clients.add(websocket)
    print(f"Clients online: {len(connected_clients)}")

    try:
        async for message in websocket:
            print(f"Received: {message}")
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print(f"ConnectionClosedError — client dropped.")
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client disconnected normally.")
    finally:
        connected_clients.discard(websocket)
        print(f"Cleaned up client connection. -- Clients online: {len(connected_clients)}")

async def main():
    async with websockets.serve(handle_client, "localhost", 12345):
        print("Server running on ws://localhost:12345")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())