# Generated by Django 4.0.1 on 2023-12-05 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_activity_date_end_alter_activity_date_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_planned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activity',
            name='length',
            field=models.DurationField(null=True),
        ),
    ]
