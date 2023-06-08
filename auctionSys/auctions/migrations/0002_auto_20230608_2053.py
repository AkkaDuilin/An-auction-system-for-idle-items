# Generated by Django 2.1.5 on 2023-06-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidder',
            name='auction_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='auctioninfo',
            name='auction_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='auctioninfo',
            name='deposit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
