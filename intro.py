# Student Grade Management System
# A desktop application for managing student records and grades


import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

student_data = []
FILENAME = "students.csv"

def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

# Function to save data to CSV file
def save_to_csv():
    """Save all student data to CSV file"""
    try:
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Roll No", "Name", "Marks", "Grade"])
            for student in student_data:
                writer.writerow([student['roll'], student['name'], student['marks'], student['grade']])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

# Function to load data from CSV file
def load_from_csv():
    """Load student data from CSV file on startup"""
    global student_data
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'r') as file:
                reader = csv.DictReader(file)
                student_data = []
                for row in reader:
                    student_data.append({
                        'roll': row['Roll No'],
                        'name': row['Name'],
                        'marks': int(row['Marks']),
                        'grade': row['Grade']
                    })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

# Function to add new student
def add_student():
    """Add a new student record"""
    roll = entry_roll.get().strip()
    name = entry_name.get().strip()
    marks_str = entry_marks.get().strip()
    
    # Validation
    if not roll or not name or not marks_str:
        messagebox.showwarning("Warning", "All fields are required!")
        return
    
    # Check for duplicate roll number
    for student in student_data:
        if student['roll'] == roll:
            messagebox.showwarning("Warning", "Roll number already exists!")
            return
    
    try:
        marks = int(marks_str)
        if marks < 0 or marks > 100:
            messagebox.showwarning("Warning", "Marks should be between 0 and 100!")
            return
    except ValueError:
        messagebox.showwarning("Warning", "Marks should be a valid number!")
        return
    
    # Calculate grade and add student
    grade = calculate_grade(marks)
    student_data.append({
        'roll': roll,
        'name': name,
        'marks': marks,
        'grade': grade
    })
    
    save_to_csv()
    clear_entries()
    view_all_students()
    messagebox.showinfo("Success", "Student added successfully!")

# Function to update student record
def update_student():
    """Update selected student record"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to update!")
        return
    
    roll = entry_roll.get().strip()
    name = entry_name.get().strip()
    marks_str = entry_marks.get().strip()
    
    if not roll or not name or not marks_str:
        messagebox.showwarning("Warning", "All fields are required!")
        return
    
    try:
        marks = int(marks_str)
        if marks < 0 or marks > 100:
            messagebox.showwarning("Warning", "Marks should be between 0 and 100!")
            return
    except ValueError:
        messagebox.showwarning("Warning", "Marks should be a valid number!")
        return
    
    # Update student in the list
    item = tree.item(selected[0])
    old_roll = item['values'][0]
    
    for i, student in enumerate(student_data):
        if student['roll'] == old_roll:
            grade = calculate_grade(marks)
            student_data[i] = {
                'roll': roll,
                'name': name,
                'marks': marks,
                'grade': grade
            }
            break
    
    save_to_csv()
    clear_entries()
    view_all_students()
    messagebox.showinfo("Success", "Student updated successfully!")

# Function to delete student record
def delete_student():
    """Delete selected student record"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete!")
        return
    
    # Confirmation dialog
    result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if not result:
        return
    
    item = tree.item(selected[0])
    roll = item['values'][0]
    
    # Remove from list
    global student_data
    student_data = [s for s in student_data if s['roll'] != roll]
    
    save_to_csv()
    view_all_students()
    clear_entries()
    messagebox.showinfo("Success", "Student deleted successfully!")

# Function to search student by roll number
def search_student():
    """Search for a student by roll number"""
    roll = entry_roll.get().strip()
    
    if not roll:
        messagebox.showwarning("Warning", "Please enter roll number to search!")
        return
    
    # Clear treeview
    for item in tree.get_children():
        tree.delete(item)
    
    found = False
    for student in student_data:
        if student['roll'] == roll:
            tree.insert('', 'end', values=(student['roll'], student['name'],student['marks'], student['grade']))
            found = True
            break
    
    if not found:
        messagebox.showinfo("Not Found", "No student found with this roll number!")
        view_all_students()

# Function to view all students
def view_all_students():
    """Display all student records in Treeview"""
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    # Insert all students
    for student in student_data:
        tree.insert('', 'end', values=(student['roll'], student['name'],student['marks'], student['grade']))

# Function to select student from tree
def on_tree_select(event):
    """Fill entry fields when a student is selected"""
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        
        clear_entries()
        entry_roll.insert(0, values[0])
        entry_name.insert(0, values[1])
        entry_marks.insert(0, values[2])

# Function to clear all entry fields
def clear_entries():
    """Clear all input fields"""
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_marks.delete(0, tk.END)

# Function to show statistics
def show_statistics():
    """Display class statistics"""
    if not student_data:
        messagebox.showinfo("Statistics", "No student data available!")
        return
    
    marks_list = [s['marks'] for s in student_data]
    avg_marks = sum(marks_list) / len(marks_list)
    highest = max(marks_list)
    lowest = min(marks_list)
    total_students = len(student_data)
    
    stats_msg = f"""Class Statistics:
    
Total Students: {total_students}
Average Marks: {avg_marks:.2f}
Highest Marks: {highest}
Lowest Marks: {lowest}"""
    
    messagebox.showinfo("Class Statistics", stats_msg)
# Create main window
root = tk.Tk()
root.title("Student Grade Management System")
root.geometry("900x600")
root.configure(bg='#f0f0f0')

# Header Label
header = tk.Label(root, text="STUDENT GRADE MANAGEMENT SYSTEM",font=('Arial', 18, 'bold'), bg='#2196F3', fg='white',padx=10, pady=15)
header.pack(fill='x')

# Input Frame
input_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
input_frame.pack(fill='x')

# Roll Number
lbl_roll = tk.Label(input_frame, text="Roll No:", font=('Arial', 11),bg='#f0f0f0')
lbl_roll.grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_roll = tk.Entry(input_frame, font=('Arial', 11), width=20)
entry_roll.grid(row=0, column=1, padx=10, pady=10)

# Name
lbl_name = tk.Label(input_frame, text="Name:", font=('Arial', 11),bg='#f0f0f0')
lbl_name.grid(row=0, column=2, padx=10, pady=10, sticky='w')
entry_name = tk.Entry(input_frame, font=('Arial', 11), width=25)
entry_name.grid(row=0, column=3, padx=10, pady=10)

# Marks
lbl_marks = tk.Label(input_frame, text="Marks:", font=('Arial', 11),bg='#f0f0f0')
lbl_marks.grid(row=0, column=4, padx=10, pady=10, sticky='w')
entry_marks = tk.Entry(input_frame, font=('Arial', 11), width=15)
entry_marks.grid(row=0, column=5, padx=10, pady=10)

# Button Frame
button_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=10)
button_frame.pack(fill='x')

# Create buttons with colors
btn_add = tk.Button(button_frame, text="Add Student", font=('Arial', 10, 'bold'),bg='#4CAF50', fg='white', width=12, command=add_student)
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_update = tk.Button(button_frame, text="Update", font=('Arial', 10, 'bold'),bg='#2196F3', fg='white', width=12, command=update_student)
btn_update.grid(row=0, column=1, padx=5, pady=5)

btn_delete = tk.Button(button_frame, text="Delete", font=('Arial', 10, 'bold'),bg='#f44336', fg='white', width=12, command=delete_student)
btn_delete.grid(row=0, column=2, padx=5, pady=5)

btn_search = tk.Button(button_frame, text="Search", font=('Arial', 10, 'bold'),bg='#FF9800', fg='white', width=12, command=search_student)
btn_search.grid(row=0, column=3, padx=5, pady=5)

btn_view = tk.Button(button_frame, text="View All", font=('Arial', 10, 'bold'),bg='#9C27B0', fg='white', width=12, command=view_all_students)
btn_view.grid(row=0, column=4, padx=5, pady=5)

btn_clear = tk.Button(button_frame, text="Clear Fields", font=('Arial', 10, 'bold'),bg='#607D8B', fg='white', width=12, command=clear_entries)
btn_clear.grid(row=0, column=5, padx=5, pady=5)

btn_stats = tk.Button(button_frame, text="Statistics", font=('Arial', 10, 'bold'),bg='#009688', fg='white', width=12, command=show_statistics)
btn_stats.grid(row=0, column=6, padx=5, pady=5)

# Treeview Frame
tree_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=10)
tree_frame.pack(fill='both', expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(tree_frame)
scrollbar.pack(side='right', fill='y')

# Treeview (Table)
tree = ttk.Treeview(tree_frame, columns=('Roll No', 'Name', 'Marks', 'Grade'),show='headings', height=12, yscrollcommand=scrollbar.set)

scrollbar.config(command=tree.yview)

# Define column headings
tree.heading('Roll No', text='Roll No')
tree.heading('Name', text='Name')
tree.heading('Marks', text='Marks')
tree.heading('Grade', text='Grade')

# Define column widths
tree.column('Roll No', width=150, anchor='center')
tree.column('Name', width=300, anchor='w')
tree.column('Marks', width=150, anchor='center')
tree.column('Grade', width=150, anchor='center')

tree.pack(fill='both', expand=True)

# Bind selection event
tree.bind('<<TreeviewSelect>>', on_tree_select)

# Footer Label
footer = tk.Label(root, text="Developed by [Your Name] | Class XII Computer Science Project",font=('Arial', 9), bg='#e0e0e0', fg='#555', pady=10)
footer.pack(fill='x', side='bottom')

# Load existing data and display
load_from_csv()
view_all_students()

