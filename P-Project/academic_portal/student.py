
from exceptions import InvalidStudentRecord

class Student:
    def __init__(self, student_id, name, marks, late_days, pass_marks, fine_rate):
        self.student_id = student_id
        self.name = name
        self.marks = marks
        self.late_days = late_days
        self.status = "Pass" if marks >= pass_marks else "Fail"
        self.fine = late_days * fine_rate

    @classmethod
    def from_row(cls, row, pass_marks, fine_rate):
        try:
            student_id = row["student_id"].strip()
            name = row["name"].strip()
            marks = float(row["marks"])
            late_days = int(row["late_days"])

            if not student_id or not name:
                raise InvalidStudentRecord("Student ID or name is missing")

            if not 0 <= marks <= 100:
                raise InvalidStudentRecord("Marks must be between 0 and 100")

            if late_days < 0:
                raise InvalidStudentRecord("Late days cannot be negative")

            return cls(
                student_id, name, marks, late_days,
                pass_marks, fine_rate
            )

        except (ValueError, KeyError) as error:
            raise InvalidStudentRecord("Invalid student data") from error
