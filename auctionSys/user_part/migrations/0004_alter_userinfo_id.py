# Generated by Django 3.2.19 on 2023-06-09 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_part', '0003_auto_20230608_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]