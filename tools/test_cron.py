import datetime
import os

def create_test_file():
    # 1. Generate the Timestamps
    # Filename format: test_20260428_215501.txt
    now = datetime.datetime.now()
    file_ts = now.strftime("%Y%m%d_%H%M%S")
    content_ts = now.strftime("%Y-%m-%d %H:%M:%S")
    
    filename = f"test_{file_ts}.txt"
    # We will place this in logs/active/ to test the rotator's future path
    filepath = os.path.join("logs", "active", filename)

    # 2. Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 3. Write the Hub-compliant test file
    with open(filepath, "w") as f:
        f.write("Header:Begin\n")
        f.write(f"FileType: Test_Log\n")
        f.write(f"Date: {now.strftime('%Y-%m-%d')}\n")
        f.write(f"Time: {now.strftime('%H:%M')}\n")
        f.write("Header:End\n\n")
        f.write("Data:Begin\n")
        f.write(f"This line written at {content_ts}\n")
        f.write("Data:End\n")

    print(f"Successfully created test file: {filepath}")

if __name__ == "__main__":
    create_test_file()