# Generated by Django 4.2.5 on 2023-12-20 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RSbayStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
