import subprocess
import pandas as pd
from pathlib import Path


result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

print("Test Output:\n", result.stdout)

test_results = []


for line in result.stdout.splitlines():
    if "::test_" in line and ("PASSED" in line or "FAILED" in line):
        parts = line.split()
        test_name = parts[1].split("::")[-1] 
        status = parts[-1].lower()  
        error_message = ""

        if status == "failed":
            #Locate detailed error message
            for failure_line in result.stdout.splitlines():
                if test_name in failure_line and " - " in failure_line:
                    error_message = failure_line.split(" - ")[-1]
                    break
        
        #Append
        test_results.append({
            "test_name": test_name,
            "status": status,
            "error_message": error_message
        })


df = pd.DataFrame(test_results)


csv_path = Path("data.csv")
if csv_path.exists():
    df.to_csv(csv_path, mode="a", index=False, header=False)
else:
    df.to_csv(csv_path, index=False)

print("✅ data.csv updated successfully.")


# Save results to data.csv
file_exists = Path("data.csv").exists()
df.to_csv("data.csv", mode="a", index=False, header=not file_exists)

print("data.csv updated successfully.")
