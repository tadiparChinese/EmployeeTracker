# Generated by Django 3.2.7 on 2021-09-17 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employeeinfo_workhour_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeinfo',
            name='fixed_login_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employeeinfo',
            name='fixed_logout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
