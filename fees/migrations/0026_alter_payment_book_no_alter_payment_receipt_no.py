# Generated by Django 5.0.6 on 2024-08-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0025_payment_book_no_student_father_name_student_section_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='book_no',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt_no',
            field=models.CharField(max_length=10),
        ),
    ]
