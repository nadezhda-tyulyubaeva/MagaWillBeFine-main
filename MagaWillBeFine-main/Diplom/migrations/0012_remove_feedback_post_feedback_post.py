# Generated by Django 4.2.7 on 2024-05-18 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Diplom', '0011_post_date_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='Post',
        ),
        migrations.CreateModel(
            name='Feedback_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Feedback', models.TextField(blank=True, null=True)),
                ('Time_Submit', models.DateTimeField(blank=True, null=True)),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diplom.post')),
                ('Profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diplom.profile')),
            ],
        ),
    ]