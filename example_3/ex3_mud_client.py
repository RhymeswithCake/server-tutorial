# mud_client.py
import socket
import threading

HOST = 'localhost'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg, end='')
        except:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        try:
            while True:
                msg = input()
                if msg.strip().lower() == "/quit":
                    sock.sendall(b"/quit\n")
                    break
                sock.sendall((msg + '\n').encode())
        except (EOFError, KeyboardInterrupt):
            sock.sendall(b"/quit\n")

if __name__ == "__main__":
    main()
