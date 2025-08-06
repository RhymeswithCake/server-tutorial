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
        print("ConnectionClosedError — client dropped.")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected normally.")
    finally:
        connected_clients.discard(websocket)
        print(f"Cleaned up client connection. -- Clients online: {len(connected_clients)}")

async def shutdown():
    print("Shutting down server...")

    for client in connected_clients.copy():
        await client.close()
        connected_clients.discard(client)

    print("All client connections closed.")

async def main():
    server = await websockets.serve(handle_client, "localhost", 12345)
    print("Server running on ws://localhost:12345 — Press Ctrl+C to stop.")

    try:
        await asyncio.Future()  # Runs forever until interrupted
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected.")
    finally:
        await shutdown()
        server.close()
        await server.wait_closed()
        print("Server shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nForce exit before startup completed.")