# Generated by Django 3.0.6 on 2020-05-17 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20200518_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='biography',
            field=models.TextField(max_length=10000, null=True, verbose_name='Биография'),
        ),
    ]
