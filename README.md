# repo

This Python code creates a simple Student Grade Management System as a desktop application using the Tkinter library for the graphical user interface (GUI). It lets a user manage student records, including roll number, name, marks, and calculated grade.

Core Functionality
Data Storage: It uses a global list named student_data to hold all student records. Each record is a Python dictionary with keys for 'roll', 'name', 'marks', and 'grade'.
File Management: It saves and loads this student data to and from a CSV file named students.csv to ensure data persistence between sessions.
The load_from_csv function runs when the application starts, pulling in any previously saved data.
The save_to_csv function is called after any data modification (add, update, delete).
Grade Calculation: The calculate_grade function takes a student's marks and assigns a letter grade (A+, A, B+, etc.) based on standard thresholds (e.g., 90+ is A+, 80-89 is A).

User Interface (GUI) Features
The application presents a user-friendly interface with several key functions:
Input Fields: Text boxes are provided for entering the student's Roll No, Name, and Marks.
Action Buttons:
Add Student: Takes the input, validates the data (checks for completeness, valid marks 0-100, and duplicate roll numbers), calculates the grade, and adds the new record.
Update: Requires selecting a student from the list, takes the updated information from the input fields, and modifies the existing record.
Delete: Requires selecting a student and shows a confirmation dialog before removing the record.
Search: Allows a user to search for a student by entering their Roll No.
View All: Refreshes the display to show all current records.
Clear Fields: Wipes the text from the input boxes.
Statistics: Calculates and displays a summary, including the Total Students, Average Marks, Highest Marks, and Lowest Marks in a pop-up box.
Data Display: Student records are displayed in a clean, scrollable table format using a ttk.Treeview widget, showing Roll No, Name, Marks, and Grade. Clicking on a row in the table automatically fills the input fields with that student's details, making it easy to update or delete.

