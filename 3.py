import sqlite3

class EmployeeDB:
    def __init__(self):
        self.conn = sqlite3.connect("employees.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employee(
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            dept TEXT,
                            salary REAL)""")
        self.conn.commit()

    def add(self, id, name, dept, salary):
        self.cur.execute("INSERT INTO employee VALUES(?,?,?,?)", (id, name, dept, salary))
        self.conn.commit()
        print("Employee added!")

    def view(self):
        self.cur.execute("SELECT * FROM employee")
        for row in self.cur.fetchall():
            print(row)

    def update(self, id, name, dept, salary):
        self.cur.execute("UPDATE employee SET name=?, dept=?, salary=? WHERE id=?",
                         (name, dept, salary, id))
        self.conn.commit()
        print("Employee updated!")

    def delete(self, id):
        self.cur.execute("DELETE FROM employee WHERE id=?", (id,))
        self.conn.commit()
        print("Employee deleted!")

# ---------------- MENU ----------------
db = EmployeeDB()

while True:
    print("\n--- Employee Menu ---")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        i = int(input("ID: "))
        n = input("Name: ")
        d = input("Dept: ")
        s = float(input("Salary: "))
        db.add(i, n, d, s)

    elif ch == "2":
        db.view()

    elif ch == "3":
        i = int(input("ID to update: "))
        n = input("New Name: ")
        d = input("New Dept: ")
        s = float(input("New Salary: "))
        db.update(i, n, d, s)

    elif ch == "4":
        i = int(input("ID to delete: "))
        db.delete(i)

    elif ch == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
