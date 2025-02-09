import subprocess
import pandas as pd
from pathlib import Path

# Run tests and capture output
result = subprocess.run(["pytest"], capture_output=True, text=True)

# Debug: Print the test output
print("Test Output:")
print(result.stdout)

# Parse test results
test_results = []
for line in result.stdout.splitlines():
    if "FAILED" in line:
        test_name = line.split()[0]  # Extract test name
        error_message = line.split(" - ")[-1]  # Extract error message
        test_results.append({"test_name": test_name, "result": "failed", "error_message": error_message})
    elif "PASSED" in line:
        test_name = line.split()[0]  # Extract test name
        test_results.append({"test_name": test_name, "result": "passed", "error_message": ""})

# Debug: Print the parsed results
print("Parsed Results:")
print(test_results)

# Save results to data.csv
df = pd.DataFrame(test_results)
if Path("data.csv").exists():
    # Append to file if it exists
    df.to_csv("data.csv", mode="a", index=False, header=False)
    print("Appended results to data.csv")
else:
    # Create new file if it doesn't exist
    df.to_csv("data.csv", index=False)
    print("Created new data.csv")

# Debug: Confirm file creation/update
print("data.csv updated successfully.")
