# Generated by Django 4.2.9 on 2024-07-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_computer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='user',
            field=models.ManyToManyField(blank=True, limit_choices_to={'user_type': 'User'}, null=True, related_name='user_computers', to='home.username'),
        ),
    ]
