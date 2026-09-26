import sqlite3

class EmpDB:
    def __init__(self):
        self.conn = sqlite3.connect("emp.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS emp (id INTEGER PRIMARY KEY,name TEXT,age INTEGER,dept TEXT)""")
        self.conn.commit()

    def add(self, name, age, dept):
        self.cur.execute("INSERT INTO emp(name, age, dept) VALUES(?,?,?)", (name, age, dept))
        self.conn.commit()
        print("Employee added ")

    def show(self):
        self.cur.execute("SELECT id, name, age, dept FROM emp")
        data = self.cur.fetchall()
        if not data:
            print("No records found.")
        else:
            for row in data:
                print(row)

    def update(self, eid, name, age, dept):
        AB = "UPDATE emp SET name=?, age=?, dept=? WHERE id=?"
        CD = (name, age, dept, eid)
        self.cur.execute(AB, CD)
        self.conn.commit()
        print("Employee updated ")

    def delete(self, eid):
        self.cur.execute("DELETE FROM emp WHERE id=?", (eid,))
        self.conn.commit()
        print("Employee deleted!")
    def __del__(self):
        self.conn.close()

def main():
    db = EmpDB()
    while True:
        print("\n  Employee Menu   ")
        print("1. Add")
        print("2. Show")
        print("3. Update")
        print("4. Delete")
        print("5. Exit")

        ch = input("Enter choice: ")
        if ch == "1":
            n = input("Name: ")
            a = int(input("Age: "))
            d = input("Dept: ")
            db.add(n, a, d)
        elif ch == "2":
            db.show()
        elif ch == "3":
            eid = int(input("Enter ID to update: "))
            n = input("New Name: ")
            a = int(input("New Age: "))
            d = input("New Dept: ")
            db.update(eid, n, a, d)
        elif ch == "4":
            eid = int(input("Enter ID to delete: "))
            db.delete(eid)
        elif ch == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "  main  ":
    main()
