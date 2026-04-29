import os
import datetime
import argparse
import shutil

def rotate_logs(days_threshold):
    active_dir = os.path.join("logs", "active")
    archive_dir = os.path.join("logs", "archive")
    history_file = os.path.join("logs", "history.txt")
    
    # Ensure directories exist
    os.makedirs(active_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    today = datetime.date.today()
    moved_count = 0

    for filename in os.listdir(active_dir):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(active_dir, filename)
        log_date = None

        # Parse the internal Header for the Date tag
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.startswith("Date:"):
                        date_str = line.split(":")[1].strip()
                        log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        break
        except Exception as e:
            print(f"Skipping {filename}: Could not parse Header Date. Error: {e}")
            continue

        if log_date:
            age = (today - log_date).days
            if age >= days_threshold:
                print(f"Archiving {filename} (Age: {age} days)")
                shutil.move(filepath, os.path.join(archive_dir, filename))
                moved_count += 1

        print(f"Rotation complete. Moved {moved_count} files to archive.")

    # --- NEW HISTORY LOGGING BLOCK ---
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{now} | Automation executed | Files relocated: {moved_count}\n"

    if not os.path.exists(history_file):
        # Create a fully Hub-compliant new file
        with open(history_file, "w") as f:
            f.write("Header:Begin\n")
            f.write("FileType: Automation_History\n")
            f.write("Version: 1.0\n")
            f.write("Description: Permanent ledger for background automation scripts.\n")
            f.write("Header:End\n\n")
            f.write("Data:Begin\n")
            f.write(log_entry)
            f.write("Data:End\n")
    else:
        # Safely append inside the Data block of an existing Hub-compliant file
        with open(history_file, "r") as f:
            lines = f.readlines()
        
        # Find Data:End and insert the new line right above it
        inserted = False
        for i in range(len(lines)-1, -1, -1):
            if "Data:End" in lines[i]:
                lines.insert(i, log_entry)
                inserted = True
                break
        
        # Fallback in case the file was manually edited and Data:End is missing
        if not inserted:
            lines.append(log_entry)
            lines.append("Data:End\n")

        with open(history_file, "w") as f:
            f.writelines(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rotate Hub Session Logs based on Header Date.")
    parser.add_argument("--days", type=int, default=14, help="Threshold in days to move logs to archive.")
    args = parser.parse_args()
    
    rotate_logs(args.days)