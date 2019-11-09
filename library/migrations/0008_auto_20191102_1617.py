# Generated by Django 2.2.5 on 2019-11-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_notice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AddField(
            model_name='book',
            name='bookid',
            field=models.CharField(default=0, max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(max_length=10),
        ),
    ]
