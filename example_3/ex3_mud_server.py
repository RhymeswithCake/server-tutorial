import socket
import threading
import signal
import sys

HOST = 'localhost'
PORT = 12345

MAX_PLAYERS = 5
AVAILABLE_NAMES = ["Alice", "Bob", "Eve", "Mallory", "Trent"]
clients = {}  # conn -> name
client_lock = threading.Lock()

ROOM_DESCRIPTION = "You are in a plain room with stone walls and a torch on the wall."

server_socket = None  # global for shutdown


def broadcast_room_state():
    with client_lock:
        if not clients:
            return
        names = ", ".join(clients.values())
        message = f"\nPlayers in the room: {names}\n"
        for conn in clients:
            try:
                conn.sendall(message.encode())
            except Exception:
                pass  # ignore send errors


def broadcast_message(sender_name, message):
    with client_lock:
        for conn, name in clients.items():
            if name != sender_name:
                try:
                    conn.sendall(f"{sender_name} says: {message}\n".encode())
                except Exception:
                    pass


def handle_client(conn, addr, name):
    welcome = (
        f"Welcome, {name}!\n"
        f"Type 'help' for a list of commands.\n"
    )
    try:
        conn.sendall(welcome.encode())
        broadcast_room_state()

        while True:
            try:
                conn.sendall(b"> ")
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
            except ConnectionResetError:
                # Client disconnected abruptly
                break
            except Exception:
                break

            if not command:
                continue

            cmd = command.lower()
            if cmd == "look":
                with client_lock:
                    names = "\n".join(f"- {n}" for n in clients.values())
                try:
                    conn.sendall(f"{ROOM_DESCRIPTION}\nYou see:\n{names}\n".encode())
                except ConnectionResetError:
                    break

            elif cmd.startswith("look "):
                target = command[5:].strip()
                match = None
                with client_lock:
                    for n in clients.values():
                        if n.lower() == target.lower():
                            match = n
                            break
                try:
                    if match:
                        conn.sendall(f"You look at {match}. They look vaguely heroic.\n".encode())
                    else:
                        conn.sendall(f"There is no one here named {target}.\n".encode())
                except ConnectionResetError:
                    break

            elif cmd.startswith("say "):
                msg = command[4:].strip()
                if msg:
                    broadcast_message(name, msg)
                else:
                    try:
                        conn.sendall(b"Huh?\n")
                    except ConnectionResetError:
                        break

            elif cmd == "help":
                help_text = (
                    "\nAvailable commands:\n"
                    "  look              - Look around the room\n"
                    "  look <name>       - Look at a specific player\n"
                    "  say <message>     - Say something to everyone\n"
                    "  help              - Show this help message\n"
                    "  /quit             - Leave the game\n"
                )
                try:
                    conn.sendall(help_text.encode())
                except ConnectionResetError:
                    break

            elif cmd == "/quit":
                try:
                    conn.sendall(b"Goodbye!\n")
                except ConnectionResetError:
                    pass
                break

            else:
                try:
                    conn.sendall(b"Huh?\n")
                except ConnectionResetError:
                    break

    except Exception as e:
        print(f"Error with {name} ({addr}): {e}")

    finally:
        with client_lock:
            if conn in clients:
                del clients[conn]
                AVAILABLE_NAMES.insert(0, name)
        broadcast_room_state()
        conn.close()


def accept_connections(server):
    while True:
        try:
            conn, addr = server.accept()
        except socket.timeout:
            continue
        except OSError:
            # Server socket closed, exit loop
            break
        except Exception as e:
            print(f"Unexpected accept error: {e}")
            break

        with client_lock:
            if len(clients) >= MAX_PLAYERS or not AVAILABLE_NAMES:
                try:
                    conn.sendall(b"Server is full. Try again later.\n")
                except Exception:
                    pass
                conn.close()
                continue

            name = AVAILABLE_NAMES.pop(0)
            clients[conn] = name
            thread = threading.Thread(target=handle_client, args=(conn, addr, name), daemon=True)
            thread.start()


def shutdown_server(signum, frame):
    print("\nShutting down server gracefully...")
    with client_lock:
        for conn in list(clients.keys()):
            try:
                conn.sendall(b"Server is shutting down. Goodbye!\n")
                conn.close()
            except Exception:
                pass
        clients.clear()
    if server_socket:
        server_socket.close()
    sys.exit(0)


def main():
    global server_socket
    signal.signal(signal.SIGINT, shutdown_server)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server_socket = server
        server.bind((HOST, PORT))
        server.listen()
        server.settimeout(1.0)  # allow Ctrl+C to interrupt accept()
        print(f"Server listening on {HOST}:{PORT}")
        accept_connections(server)


if __name__ == "__main__":
    main()
