# Generated by Django 2.2.5 on 2019-10-18 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('quantity', models.IntegerField(max_length=100)),
                ('author', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
            ],
        ),
    ]
