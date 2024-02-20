# Generated by Django 4.0.1 on 2023-12-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_activity_is_planned_alter_activity_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='importance_level',
            field=models.CharField(choices=[('M', 'Must'), ('S', 'Should'), ('C', 'Could'), ('W', 'Would'), ('N', 'None'), ('n', 'DefaultNone')], default='n', max_length=1),
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, help_text='hex', max_length=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='importance_level',
            field=models.CharField(choices=[('M', 'Must'), ('S', 'Should'), ('C', 'Could'), ('W', 'Would'), ('N', 'None'), ('n', 'DefaultNone')], default='n', max_length=1),
        ),
    ]