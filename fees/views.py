from decimal import Decimal
import io
from multiprocessing import context
from venv import logger
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum
from fees.forms import  PaymentForm
from .models import Student, Payment
from django.urls import reverse
from django.db.models import F
import csv
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

import openpyxl


######################################################################################################################
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from .models import Student

def download_students_page(request):
    # Get distinct values for dropdown filters
    courses = Student.objects.values_list('course', flat=True).distinct()
    branches = Student.objects.values_list('branch', flat=True).distinct()
    
    return render(request, 'download_students.html', {
        'courses': courses,
        'branches': branches,
    })

def download_students(request):
    course = request.GET.get('course')
    branch = request.GET.get('branch')

    students = Student.objects.all()
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Students'

    headers = ['Admission Number', 'Name', 'Phone', 'Course', 'Branch', 'Monthly Fees']
    sheet.append(headers)

    for student in students:
        sheet.append([student.admission_number, student.name, student.phone, student.course, student.branch, student.monthly_fees])

    with BytesIO() as buffer:
        workbook.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'
        return response

#######################################################################################################################

def receipt_number_input(request):
    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        if receipt_no:
            return redirect(reverse('print_receipt', kwargs={'receipt_no': receipt_no}))
    return render(request, 'receipt_number_input.html')

def print_receipt(request, receipt_no):
    # Retrieve the receipt using the provided receipt number
    receipt = get_object_or_404(Payment, receipt_no=receipt_no)
    
    # Pass the receipt to the template
    context = {
        'receipt': receipt,
    }
    
    return render(request, 'print_receipt.html', context)



######################################################################################################################

from .models import Payment, Student

def student_receipt_list(request):
    selected_organization = request.GET.get('organization', '')
    selected_year = request.GET.get('year', '')

    organizations = Payment.objects.values_list('organization', flat=True).distinct()
    years = Payment.objects.values_list('year', flat=True).distinct()
    years = sorted(set(years), reverse=True)  # Ensure years are sorted and unique

    # Define the allowed receipt types and their thresholds
    allowed_receipt_types = {
        'Library Fee': 3600,
        'Hostel Fee': 12000,
        'Academic Fee': 12000,
        'Mess Fee': 48000,
        'Admission Fee': 2000,
        'Examination Fee': 400,
        'Stationary Fee': 12000,
    }

    payments = Payment.objects.all()
    if selected_organization:
        payments = payments.filter(organization=selected_organization)
    if selected_year:
        payments = payments.filter(year=selected_year)

    # Filter receipt types based on allowed receipt types
    receipt_types = [rt for rt in payments.values_list('receipt_type', flat=True).distinct() if rt in allowed_receipt_types]

    # Organize data by name and receipt type
    student_data = {}
    for payment in payments:
        student_name = payment.name
        if student_name.lower() == "atiya":
            continue  # Skip "atiya"

        # Only include data for specified receipt types
        if payment.receipt_type in allowed_receipt_types:
            if student_name not in student_data:
                student_data[student_name] = {receipt_type: 0 for receipt_type in receipt_types}
                student_data[student_name]['name'] = student_name
            student_data[student_name][payment.receipt_type] += payment.amount

    # Filter out names that don't meet the fee criteria
    filtered_data = {}
    for name, amounts in student_data.items():
        meets_criteria = any(amounts.get(rt, 0) > threshold for rt, threshold in allowed_receipt_types.items())
        if meets_criteria:
            filtered_data[name] = amounts

    context = {
        'student_data': filtered_data,
        'receipt_types': receipt_types,
        'organizations': organizations,
        'years': years,
        'selected_organization': selected_organization,
        'selected_year': selected_year,
        'allowed_receipt_types': allowed_receipt_types,  # Pass allowed receipt types and thresholds to the template
    }

    return render(request, 'student_receipt_list.html', context)





########################################################################################################################
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login page after logout
    else:
        # Handle GET requests by redirecting to the login page
        return redirect('login')

@login_required
def homepage(request):
    # Calculate the total collected amount by the logged-in user
    total_collected = Payment.objects.filter(created_by=request.user).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_collected': total_collected,
    }
    return render(request, 'homepage.html', context)


##########################################################################################################################

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment, Student
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import PaymentForm
from .models import Student, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError  # Add this import statement
from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required  # Ensures only staff members can access the view
def download_payments(request):
    payments = Payment.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Receipt No', 'Student Admission No', 'Student Name', 'Amount', 'Date', 'Created By'])

    for payment in payments:
        writer.writerow([
            payment.receipt_no,
            payment.student.admission_number,
            payment.student.name,
            payment.amount,
            payment.date,
            payment.created_by.username if payment.created_by else ''  # Use username if available, else empty string
        ])

    return response


# views.py

@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data.get('admission_number')
            amount_paid = form.cleaned_data.get('amount_paid')
            receipt_number = form.cleaned_data.get('receipt_number')
            book_no = form.cleaned_data.get('book_no')
            receipt_type = form.cleaned_data.get('receipt_type') or 'Fee'  # Default to 'Fee' if not provided

            # Attempt to get the student, but proceed even if the student does not exist
            try:
                student = Student.objects.get(admission_number=admission_number)
            except Student.DoesNotExist:
                student = None

            created_by = User.objects.get(username=request.user.username)

            # Create the payment record
            payment = Payment.objects.create(
                student=student,
                amount=amount_paid,
                receipt_no=receipt_number,
                book_no=book_no,
                created_by=created_by,
                name=student.name if student else "Unknown",
                receipt_type=receipt_type,  # Set the receipt type from the form or default
            )

            messages.success(request, 'Payment has been recorded successfully.')
            return redirect('payment_list')  # Replace 'payment_list' with your URL name for listing payments
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = PaymentForm()

    return render(request, 'make_payment.html', {'form': form})

def payment_success(request):
    admission_number = request.GET.get('admission_number')
    try:
        student = Student.objects.get(admission_number=admission_number)
        payment_details = Payment.objects.filter(student=student).order_by('-date')
        return render(request, 'payment_success.html', {
            'student': student,
            'payment_details': payment_details
        })
    except Student.DoesNotExist:
        return render(request, 'payment_success.html', {
            'error_message': 'No payment found for the provided admission number'
        })



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from .forms import PaymentUploadForm
from .models import Payment, Student
from django.contrib.auth.models import User

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Payment, Student

from django.core.exceptions import ValidationError


@login_required
@user_passes_test(lambda u: u.is_staff)
def upload_payments(request):
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)  # Assuming the data is in the first sheet
            
            # Process each row of the DataFrame
            for index, row in df.iterrows():
                receipt_no = str(row.get('Receipt No', '')).strip()
                student_admission_no = str(row.get('Student Admission No', '')).strip()  # Adjust column name
                amount_str = str(row.get('Amount', '')).strip()
                date_value = row.get('Date', None)
                created_by_username = str(row.get('Created By', '')).strip()
                receipt_type = str(row.get('receipt_type', '')).strip()
                name = str(row.get('Name', '')).strip()
                payment_method = str(row.get('Payment Method', '')).strip()  # New field for Payment Method
                organization = str(row.get('Organization', '')).strip()  # New field for Organization
                year = str(row.get('Year', '')).strip()  # New field for Year

                # Convert amount to float and handle potential conversion errors
                try:
                    amount = float(amount_str.replace(',', ''))  # Remove commas and convert to float
                except ValueError:
                    print(f"Invalid amount '{amount_str}' in row {index + 1}")
                    continue

                # Convert date to datetime.date object and handle potential conversion errors
                if pd.notna(date_value):
                    try:
                        date = pd.to_datetime(date_value).date()  # Convert to datetime.date
                    except ValueError:
                        print(f"Invalid date '{date_value}' in row {index + 1}")
                        continue
                else:
                    date = None

                # Check if student exists
                if student_admission_no:
                    try:
                        student = Student.objects.get(admission_number=student_admission_no)
                    except Student.DoesNotExist:
                        print(f"Student with admission number '{student_admission_no}' does not exist in row {index + 1}")
                        student = None
                else:
                    student = None

                # Check if user exists
                if created_by_username:
                    try:
                        created_by = User.objects.get(username=created_by_username)
                    except User.DoesNotExist:
                        print(f"User with username '{created_by_username}' does not exist in row {index + 1}")
                        created_by = None
                else:
                    created_by = None

                # Create and save Payment instance
                try:
                    payment = Payment(
                        receipt_no=receipt_no,
                        student=student,
                        amount=amount,
                        date=date,
                        created_by=created_by,
                        receipt_type=receipt_type,
                        name=name,
                        payment_method=payment_method,
                        organization=organization,  # Save the organization
                        year=year  # Save the year
                    )
                    payment.save()
                    print(f"Saved payment: {payment}")  # Print saved payment info
                except ValidationError as e:
                    print(f"Validation error for row {index + 1}: {e}")
                except Exception as e:
                    print(f"Error saving payment for row {index + 1}: {e}")

            return HttpResponse('Payments uploaded successfully')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = PaymentUploadForm()

    return render(request, 'upload_payments.html', {'form': form})


def calculate_total_due(student):
    # Placeholder function to calculate total due for a student
    total_fees = student.total_fees  # Assuming you have a field named 'total_fees' in your Student model
    total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
    total_due = total_fees - total_paid
    return total_due



def get_student_details(request):
    if request.method == 'GET':
        admission_number = request.GET.get('admission_number')
        try:
            student = Student.objects.get(admission_number=admission_number)
            total_fees_paid = sum(payment.amount for payment in student.payment_set.all())
            total_due = student.total_fees - total_fees_paid
            months_paid = total_fees_paid / student.monthly_fees
            # Round off to 2 decimal places for monetary values
            total_fees_paid = round(total_fees_paid)
            total_due = round(total_due)
            # Round off to 1 decimal place for months_paid
            months_paid = round(months_paid, 1)
            data = {
                'name': student.name,
                'phone': student.phone,
                'course': student.course,
                'branch': student.branch,
                'monthly_fees': int(student.monthly_fees),  # Convert to integer to remove decimal places
                'total_fees': int(student.total_fees),  # Convert to integer to remove decimal places
                'total_paid': total_fees_paid,
                'total_due': total_due,
                'months_paid': months_paid
            }
            return JsonResponse({'success': True, 'student': data})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Admission number not found'}, status=404)


from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa # type: ignore
from django.template.loader import get_template
from django.db.models import Sum
from django.shortcuts import render

from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment

def reports(request):
    # Fetch all students initially
    students = Student.objects.all()

    # Get unique choices for branch and section
    branch_choices = Student.BRANCH_CHOICES
    section_choices = Student._meta.get_field('section').choices
    course_choices = Student.COURSE_CHOICES  # Add this line

    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    section = request.GET.get('section', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if section:
        students = students.filter(section=section)

    # Calculate months paid for each student and filter based on the provided months_paid
    filtered_students = []
    if months_paid.isdigit():
        months_paid = int(months_paid)
        for student in students:
            total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            paid_months = total_paid / student.monthly_fees if student.monthly_fees else 0
            if paid_months < months_paid:
                filtered_students.append(student)
    else:
        filtered_students = students

    # Calculate total fees paid and outstanding fees for each filtered student
    additional_info = []
    for student in filtered_students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
        'branch_choices': branch_choices,
        'section_choices': section_choices,
        'course_choices': course_choices,  # Add this line
        'course': course,
        'branch': branch,
        'selected_section': section,
        'selected_months_paid': months_paid,
    }
    return render(request, 'reports.html', context)



def generate_pdf(request):
    # Generate the PDF
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    section = request.GET.get('section', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if section:
        students = students.filter(section=section)
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = [student for student in students if (Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0) / student.monthly_fees >= months_paid]

    additional_info = []
    for student in students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
    }

    template_path = 'pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from .models import Student, Payment

def generate_excel(request):
    # Generate the Excel
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    section = request.GET.get('section', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = students.annotate(total_paid=Sum('payment__amount')).filter(total_paid__gte=F('monthly_fees') * months_paid)

    # Create a new Workbook object
    wb = Workbook()

    # Create a worksheet
    ws = wb.active

    # Add headers to the worksheet
    headers = ['Admission Number', 'Name', 'Course', 'Branch', 'section', 'Monthly Fees', 'Total Fees', 'Total Paid', 'Total Due', 'Months Paid']
    ws.append(headers)

    # Add student data to the worksheet
    for student in students:
        total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0

        row_data = [
            student.admission_number,
            student.name,
            student.course,
            student.branch,
            student.section,
            student.monthly_fees,
            student.total_fees,
            total_paid,
            total_due,
            months_paid_count
        ]
        ws.append(row_data)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    # Save the workbook to the HTTP response
    wb.save(response)

    return response







from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'custom_password_reset.html'
    email_template_name = 'custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'custom_password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'custom_password_reset_complete.html'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, FloatField
from django.db.models import ExpressionWrapper, F
from django.shortcuts import render
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast
from collections import defaultdict  # Import defaultdict
from django.db.models import Sum, F, Count, Case, When, IntegerField


@login_required
@staff_member_required

def summary(request):
    # Get selected filters from request
    selected_organization = request.GET.get('organization', '')
    selected_year = request.GET.get('year', '')

    # Retrieve unique organizations and years for filter options
    organizations = Payment.objects.values_list('organization', flat=True).distinct()
    years = Payment.objects.values_list('year', flat=True).distinct()

    # Filter payments based on selected organization and year
    payments = Payment.objects.all()
    if selected_organization:
        payments = payments.filter(organization=selected_organization)
    if selected_year:
        payments = payments.filter(year=selected_year)

    # Annotate students with total fee and total paid
    students = Student.objects.annotate(
        total_fee=F('monthly_fees') * 12,
        total_paid=Sum('payment__amount')
    ).annotate(
        fee_due=F('total_fee') - F('total_paid'),
        fee_cleared=Case(
            When(fee_due=0, then=1),
            default=0,
            output_field=IntegerField()
        )
    )

    total_students = students.count()
    total_fees = students.aggregate(total=Sum(F('total_fee')))['total'] or 0
    collected_fees = students.aggregate(total_collected=Sum(F('total_paid')))['total_collected'] or 0
    due_fees = total_fees - collected_fees
    fee_cleared_students = students.aggregate(cleared_count=Sum(F('fee_cleared')))['cleared_count'] or 0

    # Group payments by branch, user, and section
    branch_wise_totals = payments.values('student__branch').annotate(
        total=Sum('amount')
    ).order_by('student__branch')

    user_wise_totals = payments.values('created_by__username').annotate(
        total=Sum('amount')
    ).order_by('created_by__username')

    class_wise_totals = payments.values('student__section').annotate(
        total=Sum('amount')
    ).order_by('student__section')

    # Context for rendering the template
    context = {
        'total_students': total_students,
        'total_fees': total_fees,
        'collected_fees': collected_fees,
        'due_fees': due_fees,
        'fee_cleared_students': fee_cleared_students,
        'branch_wise_totals': branch_wise_totals,
        'user_wise_totals': user_wise_totals,
        'class_wise_totals': class_wise_totals,
        'organizations': organizations,
        'years': years,
        'selected_organization': selected_organization,
        'selected_year': selected_year,
    }

    return render(request, 'summary.html', context)



############################################################################################################################\



@login_required
def user_payments(request):
    # Get payments made by the currently logged-in user
    user_payments = Payment.objects.filter(created_by=request.user).order_by('-date')

    context = {
        'user_payments': user_payments,
    }
    return render(request, 'user_payments.html', context)



from django.db.models import Sum

def student_payment_report(request):
    if request.method == 'POST':
        admission_number = request.POST.get('admission_number')
        try:
            student = Student.objects.get(admission_number=admission_number)
            payments = Payment.objects.filter(student=student).order_by('-date')
            
            # Fetch student attributes
            monthly_fee = student.monthly_fees
            total_fee = student.total_fees
            total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            fee_due = total_fee - total_paid

            return render(request, 'student_payment_report.html', {
                'student': student,
                'payments': payments,
                'monthly_fee': monthly_fee,
                'total_fee': total_fee,
                'total_paid': total_paid,
                'fee_due': fee_due
            })
        except Student.DoesNotExist:
            return render(request, 'student_payment_report.html', {'error_message': 'Student not found'})
    else:
        return render(request, 'student_payment_report.html')
    


# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

# views.py
import pandas as pd
from .forms import UploadFileForm
from .models import Student

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from .forms import UploadFileForm
from .models import Student

@login_required
@user_passes_test(lambda u: u.is_staff)  # Ensure only admin users can access this view
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)  # Load the file

                # List to store successful student objects for bulk insertion
                new_students = []
                success_students = []
                failed_students = []
                already_exists_students = []

                # Process the DataFrame
                for index, row in df.iterrows():
                    admission_number = row['Admission Number']
                    
                    # Check if admission number already exists
                    if Student.objects.filter(admission_number=admission_number).exists():
                        already_exists_students.append({
                            'admission_number': admission_number,
                            'name': row['Name'],
                            'reason': 'Already Exists'
                        })
                    else:
                        # Check for potential duplicates
                        if Student.objects.exclude(admission_number=admission_number).filter(
                                name=row['Name'],
                                phone=row['Phone'],
                                course=row['Course'],
                                section=row['section'],
                                branch=row['Branch'],
                                monthly_fees=row['Monthly Fees'],
                                student_type=row['Student Type']
                        ).exists():
                            failed_students.append({
                                'admission_number': admission_number,
                                'name': row['Name'],
                                'reason': 'Duplicate Number'
                            })
                        else:
                            # Add new student to the bulk create list
                            student = Student(
                                admission_number=admission_number,
                                name=row['Name'],
                                phone=row['Phone'],
                                course=row['Course'],
                                section=row['section'],
                                branch=row['Branch'],
                                monthly_fees=row['Monthly Fees'],
                                student_type=row['Student Type']
                            )
                            new_students.append(student)
                            success_students.append(student)

                # Bulk insert all new students at once
                if new_students:
                    Student.objects.bulk_create(new_students, batch_size=1000)  # Insert in batches of 1000

                # Prepare data for the template
                total_students_to_upload = len(df)
                already_exists_no = len(already_exists_students)
                failed_no = len(failed_students)
                success_no = total_students_to_upload - failed_no - already_exists_no
                newly_added_no = len(new_students)  # Newly added students count

                # Render the result
                return render(request, 'upload_result.html', {
                    'total_students_to_upload': total_students_to_upload,
                    'already_exists_no': already_exists_no,
                    'failed_no': failed_no,
                    'success_no': success_no,
                    'newly_added_no': newly_added_no,
                    'already_exists_students': already_exists_students,
                    'failed_students': failed_students,
                    'success_students': success_students,
                })
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})
