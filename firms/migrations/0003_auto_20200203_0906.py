# Generated by Django 2.2 on 2020-02-03 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firms', '0002_auto_20200203_0905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='country_id',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='manufacturer',
            old_name='country_id',
            new_name='country',
        ),
    ]
