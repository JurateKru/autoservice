# Generated by Django 4.2.1 on 2023-06-06 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0012_car_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='due_back',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='due back'),
        ),
    ]