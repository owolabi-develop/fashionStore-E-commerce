# Generated by Django 4.0.6 on 2022-08-26 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fashionStore', '0008_remove_whishlist_customer_alter_order_transction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fashionStore.state'),
        ),
    ]