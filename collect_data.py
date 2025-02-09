import subprocess
import pandas as pd
from pathlib import Path

# Run pytest in verbose mode to capture detailed output
result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

# Debug: Print the test output
print("Test Output:")
print(result.stdout)

# Parse test results
test_results = []
for line in result.stdout.splitlines():
    if "PASSED" in line or "FAILED" in line:
        parts = line.split()
        if len(parts) >= 2:
            test_name = parts[0].split("::")[-1]  # Extract test function name
            status = parts[1]  # PASSED or FAILED
            error_message = ""

            if status == "FAILED":
                # Find the corresponding error message
                for failure_line in result.stdout.splitlines():
                    if test_name in failure_line and " - " in failure_line:
                        error_message = failure_line.split(" - ")[-1]
                        break
            
            # Append the result to the list
            test_results.append({
                "test_name": test_name,
                "result": status.lower(),
                "error_message": error_message
            })

# Debug: Print parsed test results
print("Parsed Results:", test_results)

# Convert to DataFrame
df = pd.DataFrame(test_results)

# Save results to data.csv
file_exists = Path("data.csv").exists()
df.to_csv("data.csv", mode="a", index=False, header=not file_exists)

print("data.csv updated successfully.")
