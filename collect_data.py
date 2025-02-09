import subprocess
import pandas as pd
import re
from pathlib import Path

# Run tests and capture output
result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

# Parse test results
test_results = []
for line in result.stdout.splitlines():
    match = re.search(r"(test_\w+)\s+\.\.\.\s+(FAILED|PASSED)", line)
    if match:
        test_name, status = match.groups()
        error_message = ""
        if status == "FAILED":
            error_message = "Test failed"  # Placeholder, can be improved
        test_results.append({"test_name": test_name, "result": status.lower(), "error_message": error_message})

# Convert to DataFrame
df = pd.DataFrame(test_results)

# Save results to CSV (append if file exists)
csv_path = "data.csv"
if Path(csv_path).exists():
    df.to_csv(csv_path, mode="a", index=False, header=False, encoding="utf-8")
else:
    df.to_csv(csv_path, index=False, encoding="utf-8")

