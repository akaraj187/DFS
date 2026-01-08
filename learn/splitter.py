import os

def split_file(filename, chunk_size=1024):
    """
    Reads a file in binary mode and splits it into smaller parts.
    chunk_size = 1024 bytes (1KB)
    """
    # 1. Check if file exists
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return

    # 2. Read the source file in 'rb' (Read Binary) mode
    # In C++, this is like fopen(filename, "rb")
    with open(filename, 'rb') as source_file:
        part_num = 0
        while True:
            # Read a chunk of bytes
            chunk = source_file.read(chunk_size)
            
            # If chunk is empty, we are done
            if not chunk:
                break
            
            # 3. Write the chunk to a new file (e.g., my_pic.jpg_part_0)
            part_name = f"{filename}_part_{part_num}"
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            
            print(f"Created: {part_name} | Size: {len(chunk)} bytes")
            part_num += 1

    print(f"--- Splitting Complete! Created {part_num} parts. ---")

def stitch_file(original_filename, total_parts):
    """
    Reads the parts and joins them back into a new file.
    """
    restored_name = "restored_" + original_filename
    
    with open(restored_name, 'wb') as output_file:
        for i in range(total_parts):
            part_name = f"{original_filename}_part_{i}"
            
            # Read the part
            with open(part_name, 'rb') as part_input:
                chunk = part_input.read()
                output_file.write(chunk)
                
            print(f"Merged: {part_name}")
            
    print(f"--- Stitching Complete! Saved as {restored_name} ---")

# --- EXECUTION ZONE ---
# 1. Put an image (like 'test.jpg') in the same folder as this script.
# 2. Change the filename below to match your image.
target_file = "test.jpg" 

# Run the split
#split_file(target_file, chunk_size=1024 * 1024) # 1 MB chunks

# (Manually check your folder now - you will see the parts!)

# Run the stitch (Assuming we made 5 parts - update this number based on your run!)
stitch_file(target_file, 3)
