# Generated by Django 3.2.6 on 2021-09-30 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_ifood', '0002_auto_20210929_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='valor_pedido',
            field=models.FloatField(default=0.0),
        ),
    ]