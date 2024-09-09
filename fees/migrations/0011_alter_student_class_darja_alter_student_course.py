# Generated by Django 5.0.6 on 2024-06-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0010_alter_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='class_darja',
            field=models.CharField(choices=[('INTER - I', 'INTER - I'), ('INTER - II', 'INTER - II'), ('B.COM -I', 'B.COM - I'), ('B.COM -II', 'B.COM - II'), ('B.COM -III', 'B.COM - III'), ('Awwal (Alif)', 'اول (الف)'), ('Awwal (Baa)', 'اول (ب)'), ('Awwal (Jeem)', 'اول (ج)'), ('Duwwam (Alif)', 'دوم (الف)'), ('Duwwam (Baa)', 'دوم (ب)'), ('Suwwam (Alif)', 'سوم (الف)'), ('Suwwam (Baa)', 'سوم (ب)'), ('Suwwam (Jeem)', 'سوم (ج)'), ('Chahrum (Alif)', 'چهارم (الف)'), ('Chahrum (Baa)', 'چهارم (ب)'), ('Panjum', 'پنجم'), ('Mouqoof Alai', 'موقوف علیہ'), ('Daur-e-Hadees', 'دورہ حدیث'), ('Edadiya School (Alif)', 'ادادیہ اسکول (الف)'), ('Edadiya School (Baa)', 'ادادیہ اسکول (ب)'), ('Awwal School (Alif)', 'اول اسکول (الف)'), ('Awwal School (Baa)', 'اول اسکول (ب)'), ('Duwwam School (Alif)', 'دوم اسکول (الف)'), ('Duwwam School (Baa)', 'دوم اسکول (ب)'), ('Suwwam', 'سوم'), ('Chahrum', 'چهارم'), ('Hifz-Alif', 'Hifz-Alif'), ('Hifz-Baa', 'Hifz-Baa'), ('Hifz-Jeem', 'Hifz-Jeem'), ('Hifz-Daal', 'Hifz-Daal'), ('Hifz-Zaa', 'Hifz-Zaa'), ('Hifz-Haa', 'Hifz-Haa'), ('Hifz-Haah', 'Hifz-Haah'), ('Hifz-Waav', 'Hifz-Waav'), ('Nazira-Alif', 'Nazira-Alif'), ('Nazira-Baa', 'Nazira-Baa'), ('Nazira-Jeem', 'Nazira-Jeem'), ('Nazira-Daal', 'Nazira-Daal'), ('Alif', 'الف'), ('Baa', 'ب'), ('Jeem', 'ج'), ('Daal', 'د'), ('Toa', 'ط')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('Mahade Ashraf', 'Mahade Ashraf'), ('معہد ابرار', 'معہد ابرار'), ('حفظ', 'حفظ'), ('ناظرہ', 'ناظرہ'), ('معہد علیم', 'معہد علیم'), ('معہد قاسم', 'معہد قاسم')], max_length=100),
        ),
    ]
