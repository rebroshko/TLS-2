# Generated by Django 4.0 on 2022-01-11 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_calendar_alter_post_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Calendar',
        ),
    ]