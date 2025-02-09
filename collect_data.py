import subprocess
import pandas as pd
from pathlib import Path
import re

# Run pytest with detailed error output
result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

# Debug: Print the test output
print("Test Output:\n", result.stdout)

# Initialize list for test results
test_results = []
error_messages = {}

# Extract assertion errors from pytest output
for line in result.stdout.splitlines():
    match = re.search(r"(test_\w+)\s+FAILED", line)
    if match:
        test_name = match.group(1)
        error_messages[test_name] = ""  # Initialize error message

    elif "assert" in line:  # Find assertion errors
        for test in error_messages:
            if not error_messages[test]:  # Store the first matching error message
                error_messages[test] = "AssertionError: " + line.strip()
                break

# Process pytest output to get test results
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

# Convert results to DataFrame
df = pd.DataFrame(test_results)

# Save to CSV
csv_path = Path("data.csv")
if csv_path.exists():
    df.to_csv(csv_path, mode="a", index=False, header=False)
else:
    df.to_csv(csv_path, index=False)

print("✅ data.csv updated successfully.")
