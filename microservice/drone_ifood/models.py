from django.db import models
from django.utils import timezone

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=30, unique=True, primary_key=True)
    rua = models.CharField(max_length=30)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=30)
    telefone = models.IntegerField()

    def __str__(self):
        return self.nome

class Restaurante(models.Model):
    nome = models.CharField(max_length=30, unique=True, primary_key=True)
    rua = models.CharField(max_length=30)
    numero = models.IntegerField(default=0)
    telefone = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Drone(models.Model):
    nome_drone = models.CharField(max_length=30, unique=True, primary_key=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    em_voo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_drone

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    tempo_entrega = models.IntegerField(default=0)
    descricao = models.CharField(default="", max_length=30)
    valor_pedido = models.FloatField(default=0.0)
    data_pedido = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'restaurante', 'data_pedido'], name='id_pedido')
        ]

    def __str__(self):
        return str(self.cliente) + ' ' + str(self.restaurante) + ' ' + str(self.data_pedido)


