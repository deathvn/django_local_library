# Generated by Django 3.1.7 on 2021-03-05 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210305_0930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='gen',
            new_name='genre',
        ),
    ]
