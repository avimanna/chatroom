import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Usage: python client.py <IP> <Port>")
    sys.exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.connect((IP_address, Port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            if not message:
                print("Disconnected from server")
                sys.exit()
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.flush()