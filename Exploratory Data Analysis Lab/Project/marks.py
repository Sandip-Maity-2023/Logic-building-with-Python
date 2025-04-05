import pandas as pd

# Load the CSV file
df = pd.read_csv('students_marks.csv')

# Function to calculate internal marks
def calculate_internal_marks(row):
    # Fetch all test marks
    tests = [row['Class Test 1'], row['Class Test 2'], row['Class Test 3'], row['Class Test 4']]
    attendance = row['Attendance']
    grade = row['Overall Class Grade'] if pd.notnull(row['Overall Class Grade']) else 'C'  # Default to 'C' if missing

    # If attendance = 0 and all tests = 0, return "NA" (for any grade A, B, C)
    if attendance == 0 and all(test == 0 for test in tests):
        return "NA"

    # Process absent tests (0 marks) as per conditions
    adjusted_tests = []
    for test in tests:
        if test == 0:
            if attendance >= 85:
                adjusted_tests.append({'A': 18, 'B': 17, 'C': 16}.get(grade, 16))
            elif 75 <= attendance < 85:
                adjusted_tests.append({'A': 16, 'B': 15, 'C': 14}.get(grade, 14))
            else:
                adjusted_tests.append(test)  # Keep 0 if attendance is low
        else:
            adjusted_tests.append(test)

    # Select the best 3 tests after adjustment
    tests_sorted = sorted(adjusted_tests, reverse=True)
    best_3_tests = tests_sorted[:3]
    test_avg = sum(best_3_tests) / 3

    # Scale Class Test Marks to 40
    test_marks = (test_avg / 20) * 40  # Test component is out of 40

    # Attendance Marks Calculation (Max 5)
    if attendance >= 80:
        attendance_marks = 5
    elif attendance >= 75:
        attendance_marks = 3
    else:
        attendance_marks = 2

    # Class Performance Marks based on Grade (Max 5)
    grade_performance_marks = {'A': 5, 'B': 4, 'C': 3}
    performance_marks = grade_performance_marks.get(grade, 3) if attendance > 0 else 0  # No marks if attendance is 0

    # Total Internal Marks out of 50
    internal_marks = test_marks + attendance_marks + performance_marks
    return round(internal_marks, 2)

# Apply the function to each student
df['Internal Marks (out of 50)'] = df.apply(calculate_internal_marks, axis=1)

# Export result to a new CSV file
df.to_csv('Final_Internal_Marks.csv', index=False)

# Print the output for review
print(df[['Name', 'Roll', 'Class Test 1', 'Class Test 2', 'Class Test 3', 'Class Test 4', 'Attendance', 'Overall Class Grade', 'Internal Marks (out of 50)']])
