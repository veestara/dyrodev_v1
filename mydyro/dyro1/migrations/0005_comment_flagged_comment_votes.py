# Generated by Django 5.0.6 on 2024-06-28 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dyro1', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]