# Generated by Django 4.2.16 on 2024-12-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.TextField(blank=True, null=True),
        ),
    ]
