# Generated by Django 5.1.2 on 2024-11-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0005_address_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
