# Example 3: chat_client

import asyncio
import websockets
import aioconsole # <-- this is like asyncio but for inputs, it makes it so we dont hang and wait for input

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
                    if msg.lower() == "/quit": # <-- a command to quit the chat for the user you can only find by reading the code
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
        print(f"Unexpected error: {e}") # <-- this catches all weird shit so we can handle it. as you can see I needed it above to handle ctrl-c properly.

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nExited.")