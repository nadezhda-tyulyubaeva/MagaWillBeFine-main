# Generated by Django 5.0.6 on 2024-05-16 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diplom', '0007_status_alter_event_image_alter_post_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
