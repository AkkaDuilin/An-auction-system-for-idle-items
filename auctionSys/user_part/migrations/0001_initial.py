# Generated by Django 2.0.4 on 2023-06-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_pwd', models.CharField(max_length=40)),
                ('user_email', models.CharField(max_length=40)),
                ('user_rman', models.CharField(default='', max_length=20)),
                ('user_address', models.CharField(default='', max_length=100)),
                ('user_mnumber', models.CharField(default='', max_length=6)),
                ('user_pnumber', models.CharField(default='', max_length=11)),
                ('deposit_balance', models.IntegerField(default=0)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]