# Generated by Django 2.2.2 on 2020-04-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0007_auto_20200416_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='corrosion_rate',
            name='corrosion_rate',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
