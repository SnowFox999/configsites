# Generated by Django 4.2.9 on 2024-07-05 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_computer_addsettings_alter_computer_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_computer',
            name='text',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
