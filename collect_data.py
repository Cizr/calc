import subprocess
import pandas as pd
from pathlib import Path

# Run tests and capture output
result = subprocess.run(["pytest"], capture_output=True, text=True)

# Debug: Print the test output
print("Test Output:")
print(result.stdout)

# Parse test results
# Parse test results
test_results = []
for line in result.stdout.splitlines():
    if "::test_" in line:  # Detect test case result lines
        parts = line.split()
        if len(parts) >= 2:  # Ensure the line has enough parts
            test_name = parts[0].split("::")[-1]  # Extract function name
            status = parts[1]  # Get test status (PASSED/FAILED)
            error_message = ""

            if status == "FAILED":
                # Find the corresponding failure message
                for failure_line in result.stdout.splitlines():
                    if test_name in failure_line and " - " in failure_line:
                        error_message = failure_line.split(" - ")[-1]
                        break
            
            # Append test result
            test_results.append({
                "test_name": test_name,
                "result": status.lower(),
                "error_message": error_message
            })

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
