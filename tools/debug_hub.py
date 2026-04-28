import os

def check_files():
    print("--- DATAHUB DIAGNOSTIC ---")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "Schema:" in content:
                        print(f"FOUND: {path}")
                        for line in content.splitlines():
                            if "Schema:" in line:
                                print(f"  -> {line.strip()}")
                            if "BuildingName" in line:
                                # Show exactly what the columns look like (with hidden chars)
                                print(f"  -> Columns: {repr(line)}")

if __name__ == "__main__":
    check_files()