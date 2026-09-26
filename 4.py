import pandas as pd

class Employee:
    def __init__(self, file="employees.csv"):
        self.file = file
        expected_columns = ["ID", "Name", "Salary"]
    def save(self):
        self.df.to_csv(self.file, index=False)

    def add(self, id, name, salary):
        row = pd.DataFrame([[id, name, salary]], columns=self.df.columns)
        self.df = pd.concat([self.df, row], ignore_index=True)
        self.save()
        print("Employee added.")

    def show(self):
        if self.df.empty:
            print("No records yet.")
        else:
            print(self.df)

    def update(self, id, name, salary):
        if id in self.df["ID"].values:
            self.df.loc[self.df["ID"] == id, ["Name", "Salary"]] = [name, salary]
            self.save()
            print("Employee updated.")
        else:
            print("ID not found.")

    def delete(self, id):
        if id in self.df["ID"].values:
            self.df = self.df[self.df["ID"] != id]
            self.save()
            print("Employee deleted.")
        else:
            print("ID not found.")
emp = Employee()

while True:
    print("\n   Employee Menu   ")
    print("1. Add Employee")
    print("2. Show All")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        emp.add(input("ID: "), input("Name: "), input("Salary: "))
    elif choice == "2":
        emp.show()
    elif choice == "3":
        emp.update(input("ID: "), input("New Name: "), input("New Salary: "))
    elif choice == "4":
        emp.delete(input("ID: "))
    elif choice == "5":
        print("Khatam")
        break
    else:
        print("Invalid choice.")

