import os

def process_xlua_file(input_path, output_path, xor_key=192):
    """XOR encrypt/decrypt a single file (same logic)"""
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        processed = bytes(b ^ xor_key for b in data)
        with open(output_path, 'wb') as f:
            f.write(processed)
        return True
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")
        return False

def batch_process(input_path, mode, xor_key=192):
    """Batch process a folder or a single file"""
    if not os.path.exists(input_path):
        print(f"Path does not exist: {input_path}")
        return

    is_file = os.path.isfile(input_path)
    action_name = "encrypted" if mode == '2' else "decrypted"
    
    if is_file:
        base_dir = os.path.dirname(input_path)
        output_dir = os.path.join(base_dir, f"{action_name}_files")
        files_to_process = [input_path]
        input_base_dir = base_dir 
    else:
        output_dir = input_path + f"_{action_name}"
        input_base_dir = input_path
        files_to_process = []
        for root, _, files in os.walk(input_path):
            for file in files:
                # Process .bytes files by default
                if file.lower().endswith('.bytes'):
                    files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        print("No .bytes files found to process!")
        return

    os.makedirs(output_dir, exist_ok=True)
    total = 0

    for in_path in files_to_process:
        if is_file:
            rel_path = os.path.basename(in_path)
        else:
            rel_path = os.path.relpath(in_path, input_base_dir)
        
        out_path = os.path.join(output_dir, rel_path)
        
        # Preserve directory structure
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        if process_xlua_file(in_path, out_path, xor_key):
            total += 1
            print(f"Processed: {rel_path}")

    print(f"\nBatch {action_name} completed! Processed {total} .bytes files")
    print(f"Results saved in: {output_dir}")

def main():
    print("="*50)
    print(" XLua .bytes Encrypt/Decrypt Tool (Drag & Drop)")
    print("="*50)
    
    while True:
        raw_path = input("\nDrag file or folder here and press Enter (q to quit): ").strip()
        
        if raw_path.lower() == 'q':
            break
            
       
        input_path = raw_path.strip("\"'")
        
        if not os.path.exists(input_path):
            print("Invalid path, please make sure you dragged correctly.")
            continue

        mode = input("Select operation - [1] Decrypt  [2] Encrypt : ").strip()
        if mode not in ['1', '2']:
            print("Invalid choice, defaulting to Decrypt [1].")
            mode = '1'

        batch_process(input_path, mode, xor_key=192)

if __name__ == "__main__":
    main()