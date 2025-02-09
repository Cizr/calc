import subprocess
import pandas as pd
from pathlib import Path

#running tests and cap the output
result = subprocess.run(["pytest"], capture_output=True, text=True)

#parsing
test_results = []
for line in result.stdout.splitlines():
    if "FAILED" in line:
        test_name = line.split()[0]  #test name exctr
        error_message = line.split(" - ")[-1]  #same but with error message
        test_results.append({"test_name": test_name, "result": "failed", "error_message": error_message})
    elif "PASSED" in line:
        test_name = line.split()[0]
        test_results.append({"test_name": test_name, "result": "passed", "error_message": ""})

#saving data.csv
df = pd.DataFrame(test_results)
if Path("data.csv").exists():
    df.to_csv("data.csv", mode="a", index=False, header=False)  #and append to file if it exists
else:
    df.to_csv("data.csv", index=False)  #new file if it doesn't exist
