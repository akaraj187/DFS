import os
import shutil # New library to help manage folders

# --- CONFIGURATION ---
NODES = ['node_1', 'node_2', 'node_3']

def setup_system():
    """Simulates booting up 3 servers (Creating folders)"""
    for node in NODES:
        os.makedirs(node, exist_ok=True)
        print(f"Server [{node}] is ONLINE.")

def distribute_file(filename, chunk_size=1024):
    """Splits file and distributes chunks across nodes"""
    
    if not os.path.exists(filename):
        print("File not found!")
        return

    print(f"--- Uploading {filename} to DFS ---")
    
    with open(filename, 'rb') as source_file:
        part_num = 0
        while True:
            chunk = source_file.read(chunk_size)
            if not chunk:
                break
            
            # --- THE ALGORITHM: ROUND ROBIN ---
            # We use the modulo operator (%) to cycle through 0, 1, 2
            node_index = part_num % len(NODES)
            current_node = NODES[node_index]
            
            # Construct the path: node_1/test.jpg_part_0
            part_name = f"{filename}_part_{part_num}"
            save_path = os.path.join(current_node, part_name)
            
            with open(save_path, 'wb') as part_file:
                part_file.write(chunk)
            
            print(f"Sent Chunk {part_num} -> {current_node}")
            part_num += 1
            
    return part_num # Return total parts so we know how to retrieve them

def retrieve_file(filename, total_parts):
    """Finds chunks in the nodes and stitches them back"""
    print(f"--- Downloading {filename} from DFS ---")
    restored_name = "restored_" + filename
    
    with open(restored_name, 'wb') as output_file:
        for i in range(total_parts):
            # Calculate where this part SHOULD be
            node_index = i % len(NODES)
            target_node = NODES[node_index]
            
            part_name = f"{filename}_part_{i}"
            path_to_read = os.path.join(target_node, part_name)
            
            # Read from that specific node
            if os.path.exists(path_to_read):
                with open(path_to_read, 'rb') as part_input:
                    output_file.write(part_input.read())
                print(f"Retrieved Chunk {i} from {target_node}")
            else:
                print(f"CRITICAL ERROR: Chunk {i} missing from {target_node}!")
                # In real life, the download would fail here.
                
    print(f"--- Download Complete! Saved as {restored_name} ---")

# --- EXECUTION ZONE ---

# 1. Boot up the servers
setup_system()

# 2. Upload the file
target_file = "test.jpg"  # Make sure this image is in the main folder
#total_chunks = distribute_file(target_file, chunk_size=1024*1024) # 1MB chunks
total_chunks=3
# 3. Download the file
retrieve_file(target_file, total_chunks)
