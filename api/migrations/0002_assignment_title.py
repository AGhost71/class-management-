# Generated by Django 4.1.7 on 2024-06-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='title',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]