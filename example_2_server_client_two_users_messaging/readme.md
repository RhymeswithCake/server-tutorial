You're going to need to update the environment as new libraries have been added:
conda env update --file environment.yml --prune

Then open three terminal windows in the example_2 folder (or navigate there).
Activate conda in each of the three terminals.
In the first terminal run the server code.
In the other two run client code.

Send messages back and forth client to client, check server to see what happens.
Then try exiting clients using the command in the client code, or ctrl-c
Try exiting the server with ctrl-c.

I've made the program behave more gracefully on disconnect to show how to do that, and to show how errors can be handled to advantage.

I'll have to think more about what Example_3 will be like.