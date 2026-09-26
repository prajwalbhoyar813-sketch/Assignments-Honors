import csv

filename = "employees.csv"
def add_employee():
    emp_id = input("enter ID: ")
    name = input("enter Name: ")
    dept = input("enter Department: ")
    salary = input("enter Salary: ")

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([emp_id, name, dept, salary])
    print("employee added ")

def view_employees():
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def update_employee():
    emp_id = input("enter ID to update: ")
    rows = []
    found = False
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        if row[0] ==emp_id:
            print("current:", row)
            row[1] = input("enter new Name: ")
            row[2] = input("enter new Department: ")
            row[3] = input("enter new Salary: ")
            found = True

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    if found:
        print("employee updated!")
    else:
        print("employee not found!")

def delete_employee():
    emp_id = input("enter id to delete: ")
    rows = []
    found = False

    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    new_rows = []
    for row in rows:
        if row[0] != emp_id:
            new_rows.append(row)
        else:
            found = True
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    if found:
        print("Employee deleted:")
    else:
        print("Employee not found :")

while True:
    print("\n    Employee Menu    ")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")

    choice = input("Enter choice: ")
    if choice =="1":
        add_employee()
    elif choice =="2":
        view_employees()
    elif choice =="3":
        update_employee()
    elif choice =="4":
        delete_employee()
    elif choice =="5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice ")