# Generated by Django 5.0.1 on 2024-02-04 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0011_alter_admin_name_alter_orderitem_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='owner',
            new_name='customer',
        ),
    ]
