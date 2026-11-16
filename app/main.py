import getpass
import os
from datetime import date

import psycopg


def get_connection():
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "students_db"),
        user=os.getenv("PGUSER", "postgres"),
        connect_timeout=5,
    )


def getAllStudents():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT student_id, first_name, last_name, email, enrollment_date "
            "FROM students ORDER BY student_id"
        ).fetchall()

    headers = ("ID", "First name", "Last name", "Email", "Enrollment date")
    display = [tuple("NULL" if value is None else str(value) for value in row)
               for row in rows]
    widths = [max(len(row[index]) for row in [headers, *display])
              for index in range(len(headers))]
    for row in [headers, *display]:
        print(" | ".join(value.ljust(width) for value, width in zip(row, widths)))
    print(f"{len(rows)} student(s).")
    return rows


def addStudent(first_name, last_name, email, enrollment_date):
    with get_connection() as connection:
        row = connection.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) "
            "VALUES (%s, %s, %s, %s) RETURNING student_id",
            (first_name, last_name, email, enrollment_date),
        ).fetchone()
    print(f"Added student with ID {row[0]}.")
    return row[0]


def updateStudentEmail(student_id, new_email):
    with get_connection() as connection:
        row = connection.execute(
            "UPDATE students SET email = %s WHERE student_id = %s "
            "RETURNING student_id",
            (new_email, student_id),
        ).fetchone()
    print(f"Updated student {student_id}." if row else f"Student {student_id} not found.")
    return row is not None


def deleteStudent(student_id):
    with get_connection() as connection:
        row = connection.execute(
            "DELETE FROM students WHERE student_id = %s RETURNING student_id",
            (student_id,),
        ).fetchone()
    print(f"Deleted student {student_id}." if row else f"Student {student_id} not found.")
    return row is not None


def read_required(prompt):
    value = input(prompt).strip()
    if not value:
        raise ValueError("This field cannot be blank.")
    return value


def read_student_id():
    student_id = int(read_required("Student ID: "))
    if not 1 <= student_id <= 2147483647:
        raise ValueError("Student ID must be between 1 and 2147483647.")
    return student_id


def read_enrollment_date():
    value = input("Enrollment date (YYYY-MM-DD, blank for NULL): ").strip()
    if not value:
        return None
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("Use YYYY-MM-DD for the enrollment date.")
    return parsed


def main():
    print("PostgreSQL Student Manager")
    if "PGPASSWORD" not in os.environ and "PGPASSFILE" not in os.environ:
        os.environ["PGPASSWORD"] = getpass.getpass("PostgreSQL password: ")

    while True:
        print("\n1. getAllStudents\n2. addStudent\n3. updateStudentEmail\n4. deleteStudent\n0. Exit")
        choice = input("Choose an operation: ").strip()
        try:
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first = read_required("First name: ")
                last = read_required("Last name: ")
                email = read_required("Email: ")
                enrolled = read_enrollment_date()
                addStudent(first, last, email, enrolled)
            elif choice == "3":
                student_id = read_student_id()
                email = read_required("New email: ")
                updateStudentEmail(student_id, email)
            elif choice == "4":
                deleteStudent(read_student_id())
            elif choice == "0":
                return
            else:
                print("Choose 0, 1, 2, 3, or 4.")
        except ValueError as error:
            print(f"Invalid input: {error}")
        except psycopg.errors.UniqueViolation:
            print("That email is already assigned to another student. No changes were saved.")
        except psycopg.OperationalError:
            print("Connection failed. Check that PostgreSQL is running and verify "
                  "the connection settings and password in the README.")
        except psycopg.Error as error:
            print(f"Database error: {error.diag.message_primary or type(error).__name__}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
