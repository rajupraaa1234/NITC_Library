# Generated by Django 2.2.5 on 2019-11-06 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20191103_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='verify',
            field=models.BooleanField(default=False),
        ),
    ]