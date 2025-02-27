import os
from django.http import HttpResponse, HttpResponseRedirect
from openpyxl import Workbook
from django.shortcuts import render
from .models import StudentResult
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

# ... (other imports and definitions)

def create_excel_sheets(request):
    student_results = StudentResult.objects.all()

    # Directory to store the generated spreadsheet
    storage_directory = 'student_spreadsheets'
    os.makedirs(storage_directory, exist_ok=True)  # Create directory if it doesn't exist

    wb = Workbook()  # Create a new Workbook (Excel file)
    ws = wb.active  # Select the active sheet

    # Assuming StudentResult model has fields like 'first_name', 'last_name', 'matric_number', etc.
    ws.append(['Name', 'Course', 'Test', 'Exam'])

    for student_result in student_results:
        # Retrieve information for the current student
        student_info = [student_result.student.admin.first_name, student_result.subject.name, student_result.test, student_result.exam]

        # Add the student's information to the spreadsheet
        ws.append(student_info)

    # Save the spreadsheet with a generic name
    file_name = "all_students_info.xlsx"
    file_path = os.path.join(storage_directory, file_name)

    # Save the workbook (Excel file) to the specified directory
    wb.save(file_path)

    return HttpResponse("Spreadsheet generated successfully.")

def view_spreadsheet(request):
    student_results = StudentResult.objects.all()

    # Assuming the generated spreadsheets are stored in 'student_spreadsheets' directory
    file_name = "all_students_info.xlsx"
    file_path = os.path.join('student_spreadsheets', file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
            return response
    else:
        return HttpResponse("Spreadsheet not found.")
