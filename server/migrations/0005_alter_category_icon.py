# Generated by Django 5.0.6 on 2024-06-21 10:21

import server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_server_banner_server_icon_alter_category_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=server.models.category_icon_upload_path),
        ),
    ]