# Generated by Django 3.2.6 on 2021-09-29 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nome', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('rua', models.CharField(max_length=30)),
                ('numero', models.IntegerField()),
                ('complemento', models.CharField(max_length=30)),
                ('telefone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('nome_drone', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('em_voo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('nome', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('rua', models.CharField(max_length=30)),
                ('numero', models.IntegerField(default=0)),
                ('telefone', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cardapio',
            fields=[
                ('restaurante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='drone_ifood.restaurante')),
                ('nome_prato', models.CharField(max_length=30)),
                ('valor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tempo_entrega', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_ifood.cliente')),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_ifood.drone')),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_ifood.restaurante')),
            ],
        ),
    ]
