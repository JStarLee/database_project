# Generated by Django 2.2.5 on 2021-12-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='photo',
            field=models.ImageField(default='#', upload_to=''),
        ),
    ]
