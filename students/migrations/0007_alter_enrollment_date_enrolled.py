# Generated by Django 4.2.3 on 2023-07-20 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_student_family_book_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='date_enrolled',
            field=models.DateField(auto_created=True),
        ),
    ]