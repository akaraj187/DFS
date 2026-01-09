import socket
import os
import time
# --- CLUSTER CONFIGURATION ---
# Node 1 = Your Phone (Check IP in Termux)
# Node 2 = Your Laptop (Localhost)
NODES = [
    {'ip': '10.161.164.115', 'port': 5001},  # <--- REPLACE WITH PHONE IP
    {'ip': '127.0.0.1',    'port': 5002}   # <--- Laptop local server
]

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
CHUNK_SIZE = 1024 * 1024 # 1MB Chunks

def send_chunk_to_node(node, filename, chunk_data, part_index):
    """
    Connects to a specific node and sends ONE chunk.
    """
    try:
        # 1. Create the unique part name (e.g., image.jpg_part_0)
        part_filename = f"{filename}_part_{part_index}"
        data_size = len(chunk_data)
        
        print(f" -> Connecting to Node {node['ip']}:{node['port']}...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5) # Don't wait forever if phone is offline
        client.connect((node['ip'], node['port']))
        
        # 2. Send Header (part_name + size)
        header = f"{part_filename}{SEPARATOR}{data_size}"
        client.send(header.encode())
        
        time.sleep(2)

        # 3. Send the actual chunk data
        client.sendall(chunk_data)
        
        print(f"  [✓] Sent {part_filename} to {node['ip']}")
        client.close()
        return True
        
    except Exception as e:
        print(f"  [X] Failed to send to {node['ip']}: {e}")
        return False

def distribute_file(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    filesize = os.path.getsize(filename)
    print(f"--- Distributing {filename} ({filesize} bytes) ---")
    
    with open(filename, 'rb') as f:
        part_index = 0
        while True:
            # Read a 1MB chunk
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            
            # Round Robin Logic:
            # Part 0 -> Node 1 (Phone)
            # Part 1 -> Node 2 (Laptop)
            # Part 2 -> Node 1 (Phone) ...
            node_idx = part_index % len(NODES)
            target_node = NODES[node_idx]
            
            print(f"\nProcessing Chunk {part_index}...")
            success = send_chunk_to_node(target_node, filename, chunk, part_index)
            
            if not success:
                print("CRITICAL: Node offline! Data lost.")
                # In a real system, we would retry with the NEXT node here (Failover)
            
            part_index += 1

    print("\n--- Distribution Complete! ---")

if __name__ == "__main__":
    # Ensure you have 'test.jpg' or a PDF in this folder
    distribute_file("test.jpg")
