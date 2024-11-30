import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_grades(report=None, grade=False, submitted=False, final=False):
    # Load the Excel file and the first sheet
    file_path = "grades.xlsx"  # Update with the correct file path
    sheet_name = "grades"
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure report column exists if `grade` or `submitted` is true
    if (grade or submitted) and report not in df.columns:
        print(f"Error: Column '{report}' not found in the dataset.")
        return

    if grade:
        # Handle grades as before
        grades = df[['Initials', report]].copy()
        grades[report] = pd.to_numeric(grades[report], errors='coerce')
        print(f"Grades for {report}:")
        print(grades)

        # Drop NaN values
        valid_grades = grades[report].dropna()

        # Remove zero values
        valid_grades = valid_grades[valid_grades > 0]

        print("\nThis analysis only considered the number of submissions (don't include zeros)")
        print("\nStatistical Analysis:")
        print(f"Number of Submissions: {valid_grades.count()}")
        print(f"Mean: {valid_grades.mean():.2f}")
        print(f"Median: {valid_grades.median():.2f}")
        print(f"Standard Deviation: {valid_grades.std():.2f}")
        print(f"Minimum: {valid_grades.min():.2f}")
        print(f"Maximum: {valid_grades.max():.2f}")

        # Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(grades[report], bins=np.arange(0, 6, 0.5), edgecolor='black', alpha=0.7)
        plt.title(f"Grade Distribution for {report}")
        plt.xlabel("Grades")
        plt.ylabel("Number of Students")
        plt.axvline(valid_grades.mean(), color='red', linestyle='dashed', label=f"Mean: {valid_grades.mean():.2f}")
        plt.axvline(valid_grades.median(), color='blue', linestyle='dashed', label=f"Median: {valid_grades.median():.2f}")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

        # Bar chart for individual grades
        plt.figure(figsize=(12, 8))
        grades.set_index('Initials')[report].plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f"Individual Grades for {report}")
        plt.xlabel("Initials")
        plt.ylabel("Grades")
        plt.axhline(valid_grades.mean(), color='red', linestyle='dashed', label=f"Mean: {valid_grades.mean():.2f}")
        plt.axhline(valid_grades.median(), color='blue', linestyle='dashed', label=f"Median: {valid_grades.median():.2f}")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()


    if submitted:
        # Handle submissions as before
        df['Submission Status'] = df[report].apply(lambda x: 'YES' if x > 0 else 'NO')
        print(f"Submission Report for {report}:")
        print(df[['Initials', report, 'Submission Status']])

        submission_counts = df['Submission Status'].value_counts()

        plt.figure(figsize=(10, 6))
        submission_counts.plot(kind='bar', color=['green', 'red'], edgecolor='black')
        plt.title(f"Submission Status for {report}")
        plt.xlabel("Submission Status")
        plt.ylabel("Number of Students")
        plt.xticks(rotation=0)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

        plt.figure(figsize=(8, 8))
        submission_counts.plot(kind='pie', autopct='%1.1f%%', labels=['YES', 'NO'], colors=['green', 'red'])
        plt.title(f"Submission Distribution for {report}")
        plt.ylabel("")
        plt.show()

    if final:
        # Ensure the required columns exist for final grade calculation
        required_columns = {'P1', 'P2', 'P3', 'Quices'}
        if not required_columns.issubset(df.columns):
            print(f"Error: Columns {required_columns - set(df.columns)} are missing for final grade calculation.")
            return
        
        # Replace NaN values in the required columns
        df[['P1', 'P2', 'P3', 'Quices']] = df[['P1', 'P2', 'P3', 'Quices']].fillna(0)

        # Calculate final grades
        df['Final'] = (df['P1'] * 0.3 + df['P2'] * 0.3 + df['P3'] * 0.25 + df['Quices'] * 0.15)

        # Display the calculated final grades
        print("Calculated Final Grades:")
        print(df[['Initials', 'Final']])

        # Statistical analysis for final grades
        final_grades = df['Final']
        print("\nFinal Grades Statistical Analysis:")
        print(f"Mean: {final_grades.mean():.2f}")
        print(f"Median: {final_grades.median():.2f}")
        print(f"Standard Deviation: {final_grades.std():.2f}")
        print(f"Minimum: {final_grades.min():.2f}")
        print(f"Maximum: {final_grades.max():.2f}")
        print(f"Number of Students: {final_grades.count()}")

        # Plot final grade distribution
        plt.figure(figsize=(10, 6))
        plt.hist(final_grades, bins=np.arange(0, 6, 0.5), edgecolor='black', alpha=0.7)
        plt.title("Final Grade Distribution")
        plt.xlabel("Final Grades")
        plt.ylabel("Number of Students")
        plt.axvline(final_grades.mean(), color='red', linestyle='dashed', label=f"Mean: {final_grades.mean():.2f}")
        plt.axvline(final_grades.median(), color='blue', linestyle='dashed', label=f"Median: {final_grades.median():.2f}")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

        # Plot bar chart for final grades
        plt.figure(figsize=(12, 8))
        df.set_index('Initials')['Final'].plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title("Final Grades for Each Student")
        plt.xlabel("Initials")
        plt.ylabel("Final Grade")
        plt.axhline(final_grades.mean(), color='red', linestyle='dashed', label=f"Mean: {final_grades.mean():.2f}")
        plt.axhline(final_grades.median(), color='blue', linestyle='dashed', label=f"Median: {final_grades.median():.2f}")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()
