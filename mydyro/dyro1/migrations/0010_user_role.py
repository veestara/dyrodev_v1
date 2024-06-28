# Generated by Django 5.0.6 on 2024-06-28 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dyro1', '0009_remove_comment_code_snippets'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('regular', 'Regular User'), ('author', 'Author'), ('admin', 'Admin')], default='regular', max_length=10),
        ),
    ]