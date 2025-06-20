import hashlib
import os
import json

def get_file_hash(file_path):
    hash_func = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return None

def save_hashes(directory, hash_file='hashes.json'):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_hashes[file_path] = get_file_hash(file_path)
    with open(hash_file, 'w') as f:
        json.dump(file_hashes, f, indent=4)
    print(f"[+] Hashes saved to {hash_file}")

def check_integrity(hash_file='hashes.json'):
    try:
        with open(hash_file, 'r') as f:
            saved_hashes = json.load(f)
    except FileNotFoundError:
        print("[-] Hash file not found. Please save hashes first.")
        return

    print("\n--- Integrity Check Results ---")
    for path, old_hash in saved_hashes.items():
        new_hash = get_file_hash(path)
        if new_hash is None:
            print(f"[!] File missing: {path}")
        elif new_hash != old_hash:
            print(f"[!] Modified: {path}")
        else:
            print(f"[OK] Unchanged: {path}")

def main():
    print("=== File Integrity Checker ===")
    print("1. Save file hashes")
    print("2. Check file integrity")
    choice = input("Enter choice (1/2): ")

    if choice == '1':
        directory = input("Enter directory path to scan: ")
        save_hashes(directory)
    elif choice == '2':
        check_integrity()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()