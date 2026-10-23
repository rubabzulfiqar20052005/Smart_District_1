
import csv
import os
import asyncio
import logging
import time
from pathlib import Path
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

from exceptions import InvalidStudentRecord
from student import Student

# Project paths and configuration
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

PASS_MARKS = int(os.getenv("PASS_MARKS", "40"))
FINE_PER_DAY = float(os.getenv("FINE_PER_DAY", "50"))

# Logging setup
logging.basicConfig(
    filename=BASE_DIR / "portal.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("AcademicPortal")


# Decorator to calculate execution time
def show_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        logger.info(
            "%s completed in %.2f seconds",
            func.__name__, time.time() - start
        )
        return result
    return wrapper


# Process and validate one student
async def process_student(row):
    await asyncio.sleep(0)

    try:
        student = Student.from_row(
            row, PASS_MARKS, FINE_PER_DAY
        )
        return student, None

    except InvalidStudentRecord as error:
        logger.error("Invalid record %s: %s", row, error)
        return None, {"Student ID": row.get("student_id", ""),
                      "Error": str(error)}


# Main async pipeline
@show_time
async def run_pipeline():
    students = []
    invalid_records = []

    input_file = BASE_DIR / "students.csv"

    with open(input_file, "r", newline="") as file:
        rows = list(csv.DictReader(file))

    results = await asyncio.gather(
        *(process_student(row) for row in rows)
    )

    for student, error in results:
        if student is not None:
            students.append(student)
        else:
            invalid_records.append(error)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_file = BASE_DIR / f"academic_report_{timestamp}.csv"
    error_file = BASE_DIR / f"invalid_records_{timestamp}.csv"

    # Save valid student report
    with open(report_file, "w", newline="") as file:
        fields = [
            "Student ID", "Name", "Marks",
            "Status", "Late Days", "Fine (Rs.)"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for student in students:
            writer.writerow({
                "Student ID": student.student_id,
                "Name": student.name,
                "Marks": student.marks,
                "Status": student.status,
                "Late Days": student.late_days,
                "Fine (Rs.)": student.fine
            })

    # Save invalid records separately
    with open(error_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Student ID", "Error"]
        )
        writer.writeheader()
        writer.writerows(invalid_records)

    failed = sum(
        1 for student in students if student.status == "Fail"
    )
    total_fines = sum(student.fine for student in students)

    logger.info("Academic reports generated successfully")

    print("\n===== ACADEMIC PORTAL =====")
    print("Total records:", len(rows))
    print("Valid students:", len(students))
    print("Invalid records:", len(invalid_records))
    print("Failed students:", failed)
    print("Total late fines: Rs.", total_fines)
    print("Academic report:", report_file.name)
    print("Invalid records report:", error_file.name)
    print("Error log: portal.log")
    print("===========================")


if __name__ == "__main__":
    try:
        asyncio.run(run_pipeline())
    except Exception:
        logger.exception("Academic Portal failed")
        print("An error occurred. Check portal.log for details.")
