import socket

import os
import time

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = '10.161.164.115'
PORT = 5001

def send_file(filename):
    filesize = os.path.getsize(filename)
    
    # 1. Connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {HOST}:{PORT}...")
    client_socket.connect((HOST, PORT))
    print("[+] Connected.")

    # 2. SEND THE HEADER (Marshalling)
    # Format: "test.jpg<SEPARATOR>50000"
    header = f"{filename}{SEPARATOR}{filesize}"
    
    # Pad the header or send it? 
    # For this simple lab, sending it directly works because recv(BUFFER) picks it up.
    client_socket.send(header.encode())
    
    # IMPORTANT: A tiny sleep or waiting for ACK is usually safer here in real apps, 
    # but for localhost, we just start sending data immediately.
    time.sleep(2)
    # 3. SEND THE DATA (The Stream)
    print(f"[+] Sending {filename} ({filesize} bytes)...")
    
    with open(filename, "rb") as f:
        while True:
            # Read 4KB chunk
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break # EOF
            
            # Send chunk
            client_socket.sendall(bytes_read)

    print("[+] Done.")
    client_socket.close()

if __name__ == "__main__":
    # Make sure 'test.jpg' exists in this folder!
    send_file("test.jpg")
