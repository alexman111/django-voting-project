# Generated by Django 3.0.6 on 2020-05-18 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0013_auto_20200518_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.FileField(blank=True, null=True, upload_to='fair/static', verbose_name='Изображение'),
        ),
    ]
