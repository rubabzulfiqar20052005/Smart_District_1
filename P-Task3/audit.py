
import csv
from datetime import datetime
from auditor import scan_folder

folder_path = "project_folder"

fine_per_day = 10

files = scan_folder(folder_path)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

audit_report = "audit_report_" + timestamp + ".csv"
penalties_report = "penalties_report_" + timestamp + ".csv"

# Audit report
with open(audit_report, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "File Name", "Size (Bytes)", "File Type",
        "Last Modified", "Days Old", "Status"
    ])

    writer.writeheader()
    writer.writerows(files)

# Penalties report
with open(penalties_report, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["File Name", "Days Old", "Fine (Rs.)"])

    for item in files:
        if item["Days Old"] > 30:
            extra_days = item["Days Old"] - 30
            fine = extra_days * fine_per_day

            writer.writerow([
                item["File Name"],
                item["Days Old"],
                fine
            ])

print("Audit completed successfully!")
print("Total files:", len(files))
print("Audit report:", audit_report)
print("Penalties report:", penalties_report)
