# Generated by Django 2.2.2 on 2020-04-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0005_auto_20200414_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='enterprise',
            field=models.CharField(default=1, max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
