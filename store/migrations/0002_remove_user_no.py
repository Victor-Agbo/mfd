# Generated by Django 4.1.4 on 2023-05-09 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='no',
        ),
    ]
