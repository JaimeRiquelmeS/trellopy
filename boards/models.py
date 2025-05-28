from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class List(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.board.title}"

class Label(models.Model):
    COLOR_CHOICES = (
        ('green', 'Verde'),
        ('yellow', 'Amarillo'),
        ('orange', 'Naranja'),
        ('red', 'Rojo'),
        ('purple', 'Morado'),
        ('blue', 'Azul'),
    )
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='green')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return f"{self.name} - {self.color}"

class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    labels = models.ManyToManyField(Label, blank=True, related_name='cards')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.list.title}"
