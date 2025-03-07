# Generated by Django 5.1.4 on 2024-12-30 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
    ]
