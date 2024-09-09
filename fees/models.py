from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    COURSE_CHOICES = [
        ('Mahade Ashraf ', 'Mahade Ashraf '),
        ('معہد علیم', 'معہد علیم'),
        ('معہد ابرار', 'معہد ابرار'),
        ('معہد قاسم', 'معہد قاسم')
        # Add other courses as needed
    ]

    BRANCH_CHOICES = [
        ('Akber Bagh', 'Akber Bagh'),
        ('Khaja Bagh', 'Khaja Bagh'),

        # Add other branches as needed
    ]

    STUDENT_TYPE_CHOICES = [
        ('Day Scholar', 'Day Scholar'),
        ('Boarder', 'Boarder'),
    ]

    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES)
    section = models.CharField(
    max_length=100,
    choices=[
        ('B.COM - I', 'B.COM - I'),
        ('B.COM - II', 'B.COM - II'),
        ('B.COM - III', 'B.COM - III'),
        ('اول اسکول (الف)', 'اول اسکول (الف)'),
        ('INTER - II', 'INTER - II'),
        ('اول (الف)', 'اول (الف)'),
        ('دوم اسکول (الف)', 'دوم اسکول (الف)'),
        ('Edadiya School (Alif)', 'Edadiya School (Alif)'),
        ('ادادیہ اسکول (الف)', 'ادادیہ اسکول (الف)'),
        ('ادادیہ اسکول (ب)', 'ادادیہ اسکول (ب)'),
        ('Awwal School (Baa)', 'Awwal School (Baa)'),
        ('اول (ب)', 'اول (ب)'),
        ('اول (ج)', 'اول (ج)'),
        ('Panjum', 'Panjum'),
        ('پنجم', 'پنجم'),
        ('چهارم', 'چهارم'),
        ('چهارم (الف)', 'چهارم (الف)'),
        ('Chahrum (Alif)', 'Chahrum (Alif)'),
        ('چهارم (ب)', 'چهارم (ب)'),
        ('دورہ حدیث', 'دورہ حدیث'),
        ('دوم (الف)', 'دوم (الف)'),
        ('دوم (ب)', 'دوم (ب)'),
        ('دوم اسکول (ب)', 'دوم اسکول (ب)'),
        ('سوم', 'سوم'),
        ('سوم (الف)', 'سوم (الف)'),
        ('سوم (ب)', 'سوم (ب)'),
        ('سوم (ج)', 'سوم (ج)'),
        ('موقوف علیہ', 'موقوف علیہ'),
        ('Hifz-Waav', 'Hifz-Waav'),
        ('Suwwam', 'Suwwam'),
        ('Duwwam (Baa)', 'Duwwam (Baa)'),
        ('Suwwam (Alif)', 'Suwwam (Alif)'),
        ('Hifz- Jeem', 'Hifz- Jeem'),
        ('Awwal (Alif)', 'Awwal (Alif)'),
        ('Hifz - Alif', 'Hifz - Alif'),
        ('Hifz - Baa', 'Hifz - Baa'),
        ('Hifz-Baa', 'Hifz-Baa'),
        ('Hifz- Daal', 'Hifz- Daal'),
        ('Hifz- Haa', 'Hifz- Haa'),
        ('Hifz-Haah', 'Hifz-Haah'),
        ('Hifz-Zaa', 'Hifz-Zaa'),
        ('Nazira-Alif', 'Nazira-Alif'),
        ('Nazira-Baa', 'Nazira-Baa'),
        ('Nazira-Daal', 'Nazira-Daal'),
        ('Nazira-Jeem', 'Nazira-Jeem'),
        ('Awwal (Jeem)', 'Awwal (Jeem)'),
        ('Suwwam (Jeem)', 'Suwwam (Jeem)'),
        ('Awwal School (Alif)', 'Awwal School (Alif)'),
        ('Chahrum (Baa)', 'Chahrum (Baa)'),
        ('Daur-e-Hadees', 'Daur-e-Hadees'),
        ('Duwwam School (Alif)', 'Duwwam School (Alif)'),
        ('Duwwam (Alif)', 'Duwwam (Alif)'),
        ('حفظ', 'حفظ'),
        ('Hifz-Alif', 'Hifz-Alif'),
        ('INTER - I', 'INTER - I'),
        ('MPC - II', 'MPC - II'),
        ('BIPC - II', 'BIPC - II'),
        ('Awwal (Baa)', 'Awwal (Baa)'),
        ('دورۂ حدیث', 'دورۂ حدیث'),
    ],
    null=True,
    blank=True
)

    monthly_fees = models.DecimalField(max_digits=10, decimal_places=2)
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPE_CHOICES, default='Boarder')


    @property
    def total_fees(self):
        return self.monthly_fees * 12

    def __str__(self):
        return f'{self.name} ({self.admission_number})'


class Payment(models.Model):
    RECEIPT_TYPE_CHOICES = [
        ('fee', 'Fee'),
        ('donation', 'Donation'),
        ('other', 'Other'),
    ]

    book_no = models.CharField(max_length=10)
    receipt_no = models.CharField(max_length=10)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_type = models.CharField(max_length=15, choices=RECEIPT_TYPE_CHOICES, default='fee')
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        unique_together = ('book_no', 'receipt_no')

    def __str__(self):
        return f'Book No: {self.book_no}, Receipt No: {self.receipt_no}'
from django.core.exceptions import ValidationError

def clean_receipt_no(self):
    receipt_no = self.cleaned_data['receipt_no']
    if not (1 <= int(receipt_no) <= 50):
        raise ValidationError('Receipt number must be between 1 and 50.')
    return receipt_no
