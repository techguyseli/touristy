# Generated by Django 4.0.3 on 2022-05-25 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_favorite_user_alter_plan_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stop',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='stop',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='service',
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
        migrations.DeleteModel(
            name='Stop',
        ),
    ]
