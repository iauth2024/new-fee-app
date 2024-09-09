from django.contrib import admin
from .models import Student, Payment

class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'name', 'phone', 'course', 'branch', 'section', 'monthly_fees', 'student_type']
    list_filter = ['course', 'branch', 'section', 'student_type']
    search_fields = ['admission_number', 'name', 'phone']

admin.site.register(Student, StudentAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_no', 'student', 'amount', 'date', 'created_by', 'receipt_type', 'name', 'payment_method', 'organization', 'year')
    search_fields = ['student__admission_number', 'receipt_no']
