import os

NODES = ['node_1', 'node_2', 'node_3']

def setup_system():
    for node in NODES:
        os.makedirs(node, exist_ok=True)
    print("--- System Online: 3 Nodes Active ---")

def distribute_file_with_replication(filename, chunk_size=1024):
    """Saves every chunk to TWO different nodes"""
    
    if not os.path.exists(filename):
        print("File not found!")
        return 0

    print(f"--- Uploading {filename} (Replication Factor: 2) ---")
    
    with open(filename, 'rb') as source_file:
        part_num = 0
        while True:
            chunk = source_file.read(chunk_size)
            if not chunk:
                break
            
            # 1. Primary Node (Standard Round Robin)
            primary_index = part_num % len(NODES)
            primary_node = NODES[primary_index]
            
            # 2. Backup Node (The next node in the list)
            # If Primary is Node 1, Backup is Node 2. If Primary is Node 3, Backup is Node 1.
            backup_index = (primary_index + 1) % len(NODES)
            backup_node = NODES[backup_index]
            
            part_name = f"{filename}_part_{part_num}"
            
            # --- WRITE TO PRIMARY ---
            path_primary = os.path.join(primary_node, part_name)
            with open(path_primary, 'wb') as f:
                f.write(chunk)
                
            # --- WRITE TO BACKUP ---
            path_backup = os.path.join(backup_node, part_name)
            with open(path_backup, 'wb') as f:
                f.write(chunk)
            
            print(f"Chunk {part_num} -> {primary_node} [PRIMARY] & {backup_node} [BACKUP]")
            part_num += 1
            
    return part_num

def retrieve_file_smart(filename, total_parts):
    """Tries to read from Primary. If missing, automatically reads from Backup."""
    print(f"\n--- Downloading {filename} with Failover ---")
    restored_name = "restored_" + filename
    
    with open(restored_name, 'wb') as output_file:
        for i in range(total_parts):
            part_name = f"{filename}_part_{i}"
            
            # Calculate where it SHOULD be
            primary_index = i % len(NODES)
            backup_index = (primary_index + 1) % len(NODES)
            
            primary_node = NODES[primary_index]
            backup_node = NODES[backup_index]
            
            path_primary = os.path.join(primary_node, part_name)
            path_backup = os.path.join(backup_node, part_name)
            
            # --- THE INTELLIGENCE (Failover Logic) ---
            if os.path.exists(path_primary):
                # Happy Path: Primary is alive
                with open(path_primary, 'rb') as f:
                    output_file.write(f.read())
                print(f"Chunk {i}: Retrieved from {primary_node}")
                
            elif os.path.exists(path_backup):
                # Failover Path: Primary is dead, using Backup
                print(f"Chunk {i}: ⚠️ PRIMARY ({primary_node}) FAILED! Recovering from BACKUP ({backup_node})...")
                with open(path_backup, 'rb') as f:
                    output_file.write(f.read())
                    
            else:
                # Disaster: Both copies are gone
                print(f"Chunk {i}: ☠️ CRITICAL FAILURE! Data lost in both nodes.")

    print(f"--- Download Complete! Saved as {restored_name} ---")

# --- EXECUTION ZONE ---
setup_system()

target_file = "test.jpg" 

# 1. Upload (Now with copies!)
#total_chunks = distribute_file_with_replication(target_file, chunk_size=1024*1024)
total_chunks=3
# RETRIEVE
retrieve_file_smart(target_file, total_chunks)
