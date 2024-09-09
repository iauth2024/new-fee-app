# forms.py

from django import forms
from .models import Payment



class PaymentForm(forms.Form):
    admission_number = forms.CharField(label="Admission Number", required=True)
    name = forms.CharField(label="Name", required=True)  # Mandatory field
    amount_paid = forms.DecimalField(label="Amount Paid", required=True)
    receipt_number = forms.CharField(label="Receipt Number", required=True)
    receipt_type = forms.CharField(label="Receipt Type", required=True)  # Mandatory field
    date = forms.DateField(label="Date", required=True)
    created_by = forms.CharField(label="Created By", required=True)
    fee_type = forms.CharField(label="Fee Type", required=True)
    payment_method = forms.CharField(label="Payment Method", required=True)
    transaction_id = forms.CharField(label="Transaction ID", required=False)


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')
class PaymentUploadForm(forms.Form):
    excel_file = forms.FileField()