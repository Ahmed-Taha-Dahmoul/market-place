# Generated by Django 4.2.3 on 2023-07-24 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_payment_id_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
