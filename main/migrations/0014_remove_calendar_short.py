# Generated by Django 4.0 on 2022-01-13 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_record_choice_rec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='short',
        ),
    ]
