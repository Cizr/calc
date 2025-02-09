import subprocess
import pandas as pd
from pathlib import Path
import re

result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

print("Test Output:\n", result.stdout)

test_results = []
error_messages = {}

    match = re.search(r"(test_\w+)\s+FAILED", line)
    if match:
        test_name = match.group(1)
        error_messages[test_name] = ""  
    elif "assert" in line:  
        for test in error_messages:
            if not error_messages[test]:  
                error_messages[test] = "AssertionError: " + line.strip()
                break

for line in result.stdout.splitlines():
    match = re.search(r"(test_\w+)\s+(PASSED|FAILED)", line)
    if match:
        test_name = match.group(1)
        status = match.group(2).lower()

        test_results.append({
            "test_name": test_name,
            "result": status,
            "error_message": error_messages.get(test_name, "") if status == "failed" else ""
        })

df = pd.DataFrame(test_results)

csv_path = Path("data.csv")
if csv_path.exists():
    df.to_csv(csv_path, mode="a", index=False, header=False)
else:
    df.to_csv(csv_path, index=False)

print("✅ data.csv updated successfully.")

file_exists = Path("data.csv").exists()
df.to_csv("data.csv", mode="a", index=False, header=not file_exists)

print("data.csv updated successfully.")
