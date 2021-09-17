#!/usr/bin/env python3
from echo_server import BUFFER_SIZE
import socket, time, sys
from multiprocessing import Process

# TO-DO: establish localhost, extern_host(google), port, buffer size
HOST = ""
G_HOST = 'www/google.com'
PORT = 8001
G_PORT = 80
BUFFER_SIZE = 1024

# TO-DP: get_remote_ip() method
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()
    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

# TO-DO: handle_request() method
def handle_request(addr, conn):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

 
def mian():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        # TO-DO: bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while True:
            # TO-DO: accept incoming connections from proxy_start, print information
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                # TO-DO: get remote IP of google, connect proxy_end to it
                remote_ip = get_remote_ip(G_HOST)
                proxy_end.connect((remote_ip, G_PORT))
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f"Sending recieved data {send_full_data} to google")
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)
                data = proxy_end.recv(BUFFER_SIZE)
                print(f"Sending received data {data} to client")
                conn.send(data)

                # TO-DO: allow for multiple connections with a Process daemon
                p = Process(target=handle_request, args=(addr, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)
            # TO-DO: close the connection
            conn.close()