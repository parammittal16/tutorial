# Generated by Django 2.0.1 on 2018-01-14 13:24

from django.db import migrations, models
import snippets.models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='language',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='linenos',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='style',
        ),
        migrations.AlterField(
            model_name='snippet',
            name='document',
            field=models.ImageField(default=None, upload_to=snippets.models.get_file_name),
        ),
    ]
