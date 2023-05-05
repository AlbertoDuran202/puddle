# Generated by Django 4.2 on 2023-05-05 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0002_order_shippingaddress_orderitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shippingaddress",
            name="order",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="item.order",
            ),
        ),
    ]