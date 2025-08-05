# Import libraries
import asyncio # this library lets you create functions that wait, explained below
import websockets # this library lets you connect between servers and clients using the websocket protocol ws:// just like http://

# The async part before the function definition defines this as an asynchronous function.
# The async command is always paired with the await command.
# How this works: An async function runs until the await command, then it waits to get a response. While this is happening
# other functions are free to run and do their thing. If this wasn't the case, your whole program would pause here and wait 
# and nothing else would update or work at the same time.
async def handle_client(websocket):
    # The websocket object thats passed in here (above, in the handle_client function) is your live connection. Since it's an object it has dot notation handles on it
    # that can be used to interrogate or interact with the live connection. 
    print("Client connected")

    # The line below is where this function pauses. This line is saying wait until I receive a message before continuing this function.
    message = await websocket.recv()
    # After a message is received the next line gets printed. While waiting for the received message, other functions can run.
    print("Received from client:", message)

    print("Done.")

async def main():
    # Here two python thingies are used, one is async the other is the 'with' command.
    # async means the same as above, we're going to wait at the await command in this function.
    # the with command is a context manager, which means that after the connection ends for any reason, it will be closed out properly.
    # if you didnt have this with command here, you would have to manually close your connection, and if your program crashed you may end
    # up with a persistently open port on your computer that anyone who knew the address to could access until you closed it. 
    # Depending on how secure you are, an infiltrator may not do much damage, but still this helps with best practice.
    async with websockets.serve(handle_client, "localhost", 12345):
        # The above line line says, asynchronously, open a websocket connection using the handle_client function to deal with input,
        # at localhost on port 12345. Which gets printed below.
        print("Server is running on ws://localhost:12345")
        await asyncio.Future()  # Run this forever. (until you shut it down or end it, at which point the context manager will close your connection)

# This line uses the asyncio packages run command to run the main function. By wrapping the main function in the asyncio.run function, the async and await commands
# mean something to python, since they are ingested by the asyncio library. Otherwise python wouldn't know what the heck they were.
asyncio.run(main())

# When all this makes sense, we'll delete all the comments and clean this up.
# Take a look at the client side code and see if you can make sense of it the way it is.