# Generated by Django 3.1.7 on 2021-03-05 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210305_0750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='data_of_death',
            new_name='date_of_death',
        ),
    ]
