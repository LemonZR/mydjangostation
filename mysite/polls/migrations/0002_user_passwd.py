# Generated by Django 3.2.5 on 2021-07-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passwd',
            field=models.CharField(default='123', max_length=20),
        ),
    ]
