# Generated by Django 2.2.5 on 2021-12-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(blank=True, choices=[('1', '男'), ('2', '女')], max_length=5, null=True),
        ),
    ]
