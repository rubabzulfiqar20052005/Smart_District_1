
import os
import csv
from datetime import datetime, timedelta

def scan_folder(folder_path):

    files = []

    for folder, subfolders, filenames in os.walk(folder_path):
        for name in filenames:

            file_path = os.path.join(folder, name)

            size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)

            modified_date = datetime.fromtimestamp(modified_time)
            days_old = (datetime.now() - modified_date).days

            if days_old > 30:
                status = "Old File"
            else:
                status = "OK"

            file_info = {
                "File Name": name,
                "Size (Bytes)": size,
                "File Type": os.path.splitext(name)[1],
                "Last Modified": modified_date.strftime("%Y-%m-%d"),
                "Days Old": days_old,
                "Status": status
            }

            files.append(file_info)

    return files
