# Generated by Django 4.0.3 on 2022-05-11 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_remove_service_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
