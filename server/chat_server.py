import socket
import select
import sys
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Usage: python chat_server.py <IP> <Port>")
    sys.exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode())
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print(f"<{addr[0]}> {message}")
                message_to_send = f"<{addr[0]}> {message}"
                broadcast(message_to_send.encode(), conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(f"{addr[0]} connected")
    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()