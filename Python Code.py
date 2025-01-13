import mysql.connector
from datetime import datetime

# Connection to MySQL database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="employee_attendance"
    )


# Function to add an employee (Create)
def add_employee(name, role_id, email):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO employees (name, role_id, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, role_id, email))
    conn.commit()
    conn.close()
    print("Employee successfully added.")

# Function to list all employees (Read)
def list_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT employees.id, employees.name, roles.name, employees.email FROM employees JOIN roles ON employees.role_id = roles.id")
    result = cursor.fetchall()
    conn.close()
    for row in result:
        print(f"ID: {row[0]}, Name: {row[1]}, Role: {row[2]}, Email: {row[3]}")

# Function to update employee data (Update)
def update_employee(employee_id, name=None, role_id=None, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    params = []

    if name:
        updates.append("name=%s")
        params.append(name)
    if role_id:
        updates.append("role_id=%s")
        params.append(role_id)
    if email:
        updates.append("email=%s")
        params.append(email)

    params.append(employee_id)

    query = f"UPDATE employees SET {', '.join(updates)} WHERE id=%s"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    print("Employee data successfully updated.")

# Function to get employee details by ID (Read)
def get_employee_by_id(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT employees.id, employees.name, roles.name, employees.email 
        FROM employees 
        JOIN roles ON employees.role_id = roles.id
        WHERE employees.id = %s
    """
    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"\n--- Employee Details ID {employee_id} ---")
        print(f"ID: {result[0]}")
        print(f"Name: {result[1]}")
        print(f"Role: {result[2]}")
        print(f"Email: {result[3]}")
    else:
        print(f"Employee with ID {employee_id} not found.")

# Function to delete an employee (Delete)
def delete_employee(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
    conn.commit()
    conn.close()
    print("Employee successfully deleted.")

# Function to add check-in attendance (Create)
def add_attendance_in(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    date_today = datetime.now().date()
    time_in = datetime.now().time()
    query = "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, date_today, f"Check-in: {time_in}"))
    conn.commit()
    conn.close()
    print("Check-in attendance successfully added.")

# Function to add check-out attendance (Create)
def add_attendance_out(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    date_today = datetime.now().date()
    time_out = datetime.now().time()
    query = "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, date_today, f"Check-out: {time_out}"))
    conn.commit()
    conn.close()
    print("Check-out attendance successfully added.")

# Function to list attendance for an employee (Read)
def list_attendance(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT date, status FROM attendance WHERE employee_id=%s"
    cursor.execute(query, (employee_id,))
    result = cursor.fetchall()
    conn.close()
    for row in result:
        print(f"Date: {row[0]}, Status: {row[1]}")

# Function to choose a role (Read)
def choose_role():
    roles = ["Director", "Manager", "Marketing", "Employee"]
    for i, role in enumerate(roles, 1):
        print(f"{i}. {role}")
    choice = int(input("Choose Role (1-4): "))
    if choice in range(1, 5):
        return choice
    else:
        print("Invalid choice. Please try again.")
        return choose_role()
    
# Employee Main  Menu
def main_menu():
    while True:
        print("\n=== Employee Attendance System ===")
        print("1. Employee Administration")
        print("2. Attendance")
        print("99. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            employee_admin_menu()
        elif choice == "2":
            attendance_menu()
        elif choice == "99":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Employee Administration Menu
def employee_admin_menu():
    while True:
        print("\n--- Employee Administration Menu ---")
        print("1. View All Employees")
        print("2. View Employee by ID")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("99. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            list_employees()
        elif choice == "2":
            employee_id = input("Enter Employee ID: ")
            get_employee_by_id(employee_id)
        elif choice == "3":
            employee_id = input("Employee ID: ")
            name = input("New name (leave blank if not changing): ")
            print("Choose new role (leave blank if not changing):")
            role_id = choose_role()
            email = input("New email (leave blank if not changing): ")
            update_employee(employee_id, name or None, role_id, email or None)
        elif choice == "4":
            employee_id = input("Employee ID: ")
            delete_employee(employee_id)
        elif choice == "99":
            return
        else:
            print("Invalid choice. Please try again.")

# Attendance Menu
def attendance_menu():
    while True:
        print("\n--- Attendance Menu ---")
        print("1. Add Check-in")
        print("2. Add Check-out")
        print("3. View Attendance")
        print("99. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            employee_id = input("Employee ID: ")
            add_attendance_in(employee_id)
        elif choice == "2":
            employee_id = input("Employee ID: ")
            add_attendance_out(employee_id)
        elif choice == "3":
            employee_id = input("Employee ID: ")
            list_attendance(employee_id)
        elif choice == "99":
            return
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
