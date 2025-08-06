# Example 3: chat_client

import asyncio
import websockets
import aioconsole

async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"\nFriend: {message}\nYou: ", end="")
    except websockets.exceptions.ConnectionClosed:
        print("\nServer disconnected.")

async def chat():
    uri = "ws://localhost:12345"
    try:
        async with websockets.connect(uri) as websocket:
            receiver = asyncio.create_task(receive_messages(websocket))
            try:
                while True:
                    msg = await aioconsole.ainput("You: ")
                    if msg.lower() == "/quit":
                        print("Disconnecting from chat...")
                        await websocket.close()  # <-- clean disconnection
                        break
                    await websocket.send(msg)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting... closing connection.")
                await websocket.close()
            finally:
                receiver.cancel()
                try:
                    await receiver
                except asyncio.CancelledError:
                    pass
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nExited.")