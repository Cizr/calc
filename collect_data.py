import subprocess
import pandas as pd
import re
from pathlib import Path

# Run pytest with verbose output
result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

# Debug: Print test output
print("Test Output:")
print(result.stdout)

# Initialize test results list
test_results = []

# Parse pytest output line by line
for line in result.stdout.splitlines():
    match = re.search(r"(test_\w+)\s+\[\d+%\]\s+(PASSED|FAILED)", line)
    if match:
        test_name, status = match.groups()
        error_message = ""

        # Capture error message for failed tests
        if status == "FAILED":
            error_line = next((l for l in result.stdout.splitlines() if test_name in l and " - " in l), None)
            if error_line:
                error_message = error_line.split(" - ")[-1]

        # Append results
        test_results.append({"test_name": test_name, "result": status.lower(), "error_message": error_message})

# Debug: Print parsed results
print("Parsed Results:")
print(test_results)

# Save results to data.csv
df = pd.DataFrame(test_results)
if Path("data.csv").exists():
    df.to_csv("data.csv", mode="a", index=False, header=False)  # Append if file exists
    print("Appended results to data.csv")
else:
    df.to_csv("data.csv", index=False)  # Create new file if not exists
    print("Created new data.csv")

# Debug: Confirm file creation/update
print("data.csv updated successfully.")
