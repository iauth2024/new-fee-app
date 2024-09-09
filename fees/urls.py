from django.urls import include, path
from . import views

from django.contrib.auth import views as auth_views
from .views import download_students, print_receipt, receipt_number_input
from .views import (
    print_receipt,
    student_receipt_list,
    upload_file, 
    download_payments, 
    upload_payments, 
    reports, 
    generate_pdf, 
    generate_excel, 
    user_payments, 
    student_payment_report, 
    CustomPasswordResetView, 
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView, 
    CustomPasswordResetCompleteView, 
    summary,
    make_payment,
    payment_success,
    get_student_details,
)

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('', views.login_view, name='login'),
    path('print-receipt/<str:receipt_no>/', print_receipt, name='print_receipt'),
    path('receipt-number/', receipt_number_input, name='receipt_number_input'),  # Add this line
    path('upload/', upload_file, name='upload_file'),
    path('download-payments/', download_payments, name='download_payments'),
    path('upload-payments/', upload_payments, name='upload_payments'),
    path('logout/', views.logout_view, name='logout'),
    path('summary/', summary, name='summary'),
    path('reports/', reports, name='reports'),
    path('student-receipts/', student_receipt_list, name='student_receipt_list'),
    path('reports/pdf/', generate_pdf, name='generate_pdf'),
    path('reports/excel/', generate_excel, name='generate_excel'),
    path('make_payment/', make_payment, name='make_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('user/payments/', user_payments, name='user_payments'),
    path('student/payment/report/', student_payment_report, name='student_payment_report'),
    path('get_student_details/', get_student_details, name='get_student_details'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot_password'),
    path('reset-password/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('download_students/', views.download_students_page, name='download_students_page'),
    path('process_download_students/', views.download_students, name='process_download_students'),  # Ensure this line is present
   
    
]
