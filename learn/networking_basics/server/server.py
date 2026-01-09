import socket
import os

HOST = '127.0.0.1'
PORT = 5002
BUFFER_SIZE = 4096  # Read 4KB at a time (Standard engineering practice)
SEPARATOR = "<SEPARATOR>"

def start_file_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"--- Node 1 Storage Online ({HOST}:{PORT}) ---")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connected to {addr}")

        # 1. READ THE HEADER FIRST
        # We expect a string like: "test.jpg<SEPARATOR>1048576"
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        
        # Remove path junk to just get "test.jpg"
        filename = os.path.basename(filename)
        filesize = int(filesize)

        print(f"[+] Incoming File: {filename} | Size: {filesize} bytes")

        # 2. READ THE DATA
        # We know exactly how many bytes to read now.
        bytes_read = 0
        with open(f"server_storage_{filename}", "wb") as f:
            while bytes_read < filesize:
                # Read chunks
                bytes_data = client_socket.recv(BUFFER_SIZE)
                if not bytes_data:
                    break # Connection lost
                
                f.write(bytes_data)
                bytes_read += len(bytes_data)
                
                # Optional: Show progress
                # print(f"  -> Received {bytes_read}/{filesize} bytes", end='\r')

        print(f"\n[+] File {filename} saved successfully.")
        client_socket.close()

if __name__ == "__main__":
    start_file_server()
