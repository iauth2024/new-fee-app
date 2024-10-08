# Generated by Django 5.0.6 on 2024-09-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0031_alter_student_branch_alter_student_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('Akber Bagh', 'Akber Bagh'), ('Khaja Bagh', 'Khaja Bagh')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('Mahade Ashraf ', 'Mahade Ashraf '), ('معہد علیم', 'معہد علیم'), ('معہد ابرار', 'معہد ابرار'), ('معہد قاسم', 'معہد قاسم')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.CharField(blank=True, choices=[('B.COM - I', 'B.COM - I'), ('B.COM - II', 'B.COM - II'), ('B.COM - III', 'B.COM - III'), ('اول اسکول (الف)', 'اول اسکول (الف)'), ('INTER - II', 'INTER - II'), ('اول (الف)', 'اول (الف)'), ('دوم اسکول (الف)', 'دوم اسکول (الف)'), ('Edadiya School (Alif)', 'Edadiya School (Alif)'), ('ادادیہ اسکول (الف)', 'ادادیہ اسکول (الف)'), ('ادادیہ اسکول (ب)', 'ادادیہ اسکول (ب)'), ('Awwal School (Baa)', 'Awwal School (Baa)'), ('اول (ب)', 'اول (ب)'), ('اول (ج)', 'اول (ج)'), ('Panjum', 'Panjum'), ('پنجم', 'پنجم'), ('چهارم', 'چهارم'), ('چهارم (الف)', 'چهارم (الف)'), ('Chahrum (Alif)', 'Chahrum (Alif)'), ('چهارم (ب)', 'چهارم (ب)'), ('دورہ حدیث', 'دورہ حدیث'), ('دوم (الف)', 'دوم (الف)'), ('دوم (ب)', 'دوم (ب)'), ('دوم اسکول (ب)', 'دوم اسکول (ب)'), ('سوم', 'سوم'), ('سوم (الف)', 'سوم (الف)'), ('سوم (ب)', 'سوم (ب)'), ('سوم (ج)', 'سوم (ج)'), ('موقوف علیہ', 'موقوف علیہ'), ('Hifz-Waav', 'Hifz-Waav'), ('Suwwam', 'Suwwam'), ('Duwwam (Baa)', 'Duwwam (Baa)'), ('Suwwam (Alif)', 'Suwwam (Alif)'), ('Hifz- Jeem', 'Hifz- Jeem'), ('Awwal (Alif)', 'Awwal (Alif)'), ('Hifz - Alif', 'Hifz - Alif'), ('Hifz - Baa', 'Hifz - Baa'), ('Hifz-Baa', 'Hifz-Baa'), ('Hifz- Daal', 'Hifz- Daal'), ('Hifz- Haa', 'Hifz- Haa'), ('Hifz-Haah', 'Hifz-Haah'), ('Hifz-Zaa', 'Hifz-Zaa'), ('Nazira-Alif', 'Nazira-Alif'), ('Nazira-Baa', 'Nazira-Baa'), ('Nazira-Daal', 'Nazira-Daal'), ('Nazira-Jeem', 'Nazira-Jeem'), ('Awwal (Jeem)', 'Awwal (Jeem)'), ('Suwwam (Jeem)', 'Suwwam (Jeem)'), ('Awwal School (Alif)', 'Awwal School (Alif)'), ('Chahrum (Baa)', 'Chahrum (Baa)'), ('Daur-e-Hadees', 'Daur-e-Hadees'), ('Duwwam School (Alif)', 'Duwwam School (Alif)'), ('Duwwam (Alif)', 'Duwwam (Alif)'), ('حفظ', 'حفظ'), ('Hifz-Alif', 'Hifz-Alif'), ('INTER - I', 'INTER - I'), ('MPC - II', 'MPC - II'), ('BIPC - II', 'BIPC - II'), ('Awwal (Baa)', 'Awwal (Baa)'), ('دورۂ حدیث', 'دورۂ حدیث')], max_length=100, null=True),
        ),
    ]
