# Generated by Django 5.0.4 on 2024-04-26 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0003_application_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
