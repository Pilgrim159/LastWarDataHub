import os

# Files that MUST use pipes for integrity
PIPE_FILES = ['BuildingData.txt', 'F1NE_Building_Status.txt', 'F1NE_BuffCalibration.txt']

def sanitize_hub():
    print("--- HUB SANITIZATION IN PROGRESS ---")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Scrub Non-Breaking Spaces
                new_content = content.replace('\xa0', ' ')
                
                # 2. Force Pipes for Status file (Converting whitespace to pipes)
                if file == 'F1NE_Building_Status.txt' and '|' not in new_content:
                    lines = new_content.splitlines()
                    processed_lines = []
                    for line in lines:
                        if 'Schema:' in line or 'Header:' in line or 'Data:' in line:
                            processed_lines.append(line)
                        elif line.strip() and not line.startswith('#'):
                            # Convert multiple spaces to a single pipe
                            parts = line.split()
                            processed_lines.append(" | ".join(parts))
                        else:
                            processed_lines.append(line)
                    new_content = "\n".join(processed_lines)

                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"FIXED: {path}")

if __name__ == "__main__":
    sanitize_hub()