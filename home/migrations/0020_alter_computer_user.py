# Generated by Django 4.2.9 on 2024-07-19 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_username_login_alter_username_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='user',
            field=models.ManyToManyField(blank=True, to='home.username'),
        ),
    ]
