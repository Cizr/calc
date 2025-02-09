import subprocess
import pandas as pd
from pathlib import Path

result = subprocess.run(["pytest"], capture_output=True, text=True)

print("Test Output:")
print(result.stdout)

test_results = []
for line in result.stdout.splitlines():
    if "FAILED" in line:
        #Extract test name and error message for failed tests
        test_name = line.split()[0]  # Extract test name
        error_message = line.split(" - ")[-1]  # Extract error message
        test_results.append({"test_name": test_name, "result": "failed", "error_message": error_message})
    elif "PASSED" in line:
        #Extract test name for passed tests
        test_name = line.split()[0]  #Extract test name
        test_results.append({"test_name": test_name, "result": "passed", "error_message": ""})
    elif "PASSED" not in line and "FAILED" not in line and "::" in line:
        #Handle cases where the test result is not explicitly marked as PASSED or FAILED
        parts = line.split("::")
        if len(parts) >= 2:
            test_name = parts[-1].split()[0]  #Extract test name
            if "PASSED" in line:
                test_results.append({"test_name": test_name, "result": "passed", "error_message": ""})
            elif "FAILED" in line:
                error_message = line.split(" - ")[-1]  #Extract error message
                test_results.append({"test_name": test_name, "result": "failed", "error_message": error_message})

print("Parsed Results:")
print(test_results)


df = pd.DataFrame(test_results)
if Path("data.csv").exists():
    #Append
    df.to_csv("data.csv", mode="a", index=False, header=False)
    print("Appended results to data.csv")
else:
    
    df.to_csv("data.csv", index=False)
    print("Created new data.csv")

print("data.csv updated successfully.")
