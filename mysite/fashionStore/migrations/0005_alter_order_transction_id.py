# Generated by Django 4.0.6 on 2022-08-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashionStore', '0004_user_subscribe_alter_order_transction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transction_id',
            field=models.CharField(default='7576566610', max_length=20, unique=True),
        ),
    ]
