# Generated by Django 4.2.7 on 2024-02-10 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0021_alter_orderitem_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='total_price',
            new_name='total_money',
        ),
    ]