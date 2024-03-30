# Generated by Django 5.0.1 on 2024-03-30 00:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_auction_highest_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="winner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="won_auctions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="auction",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_auctions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
