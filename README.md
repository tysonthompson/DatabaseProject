# PostgreSQL Student CRUD

**Video:** [demo link](https://youtu.be/zZcRPWutqD0)
https://youtu.be/zZcRPWutqD0

## Setup and run

Requires Python 3.10+, a running PostgreSQL server, and pgAdmin.

1. In pgAdmin, run `database/01_create_database.sql` on `postgres` with auto-commit enabled.
2. Connect to `students_db`; run `database/02_setup.sql` once to create and seed the table.
3. From the repository folder, run:

```powershell
python -m pip install -r requirements.txt
python -m app.main
```

No compilation needed. Defaults: `localhost:5432`, database `students_db`, user `postgres`.
Enter your password when prompted. Override defaults using `PGHOST`, `PGPORT`, `PGDATABASE`, or `PGUSER`.

## Menu

- **1:** `getAllStudents()` displays all students.
- **2:** `addStudent(...)` inserts a student and displays its ID.
- **3:** `updateStudentEmail(...)` changes the given ID's email.
- **4:** `deleteStudent(...)` deletes the given ID.
- **0:** Exit.

Dates: `YYYY-MM-DD` or blank. Verify each change in pgAdmin using `database/03_verify.sql`.
