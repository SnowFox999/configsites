# Generated by Django 4.2.9 on 2024-07-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_computer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='type',
            field=models.CharField(blank=True, choices=[('Computer1', 'Fujitsu ESPRIMO P5011'), ('Computer2', 'Fujitsu ESPRIMO G9013 ESTAR'), ('Computer3', 'Fujitsu ESPRIMO P558/E85+'), ('Computer4', 'Fujitsu ESPRIMO P557')], max_length=30, null=True),
        ),
    ]
