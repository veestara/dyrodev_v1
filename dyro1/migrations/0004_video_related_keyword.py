# Generated by Django 5.0.6 on 2024-07-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dyro1', '0003_alter_video_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='related_keyword',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]