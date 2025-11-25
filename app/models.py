from django.db import models

class Item(models.Model):
    CATEGORIAS = [
        ('Processador', 'Processador'),
        ('Placa de Vídeo', 'Placa de Vídeo'),
        ('Placa Mãe', 'Placa Mãe'),
        ('Memória RAM', 'Memória RAM'),
        ('Armazenamento', 'Armazenamento'),
        ('Fonte', 'Fonte'),
        ('Gabinete', 'Gabinete'),
        ('Cooler', 'Cooler'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    watts = models.IntegerField(default=0, help_text="Consumo em Watts (TDP)")
    comprado = models.BooleanField(default=False) # Checkbox de comprado
    links_json = models.TextField(default='[]')

    def __str__(self):
        return self.nome