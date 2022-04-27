# Generated by Django 3.2.13 on 2022-04-25 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Do not show', 'Do not show')], default='Do not show', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('Car', 'Car'), ('Motorycle', 'Motorycle'), ('Airplane', 'Airplane'), ('Helicopter', 'Helicopter'), ('Bicycle', 'Bicycle')], max_length=10),
        ),
    ]
