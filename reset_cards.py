import os
import django
import random
import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trellodj.settings')
django.setup()

from boards.models import Card, List, Board, Label
from django.contrib.auth.models import User
from django.utils import timezone

def reset_cards():
    # Limpiar todas las tarjetas existentes
    Card.objects.all().delete()
    print('Todas las tarjetas han sido eliminadas')

    # Obtener los tableros y listas existentes
    boards = Board.objects.all()
    if not boards:
        print('No hay tableros. Crea al menos un tablero primero.')
        return

    board = boards.first()
    lists = List.objects.filter(board=board)

    # Si no hay listas, crear algunas
    if not lists:
        list_names = ['Por hacer', 'En progreso', 'En revisión', 'Completado']
        for i, name in enumerate(list_names):
            List.objects.create(title=name, board=board, order=i)
        lists = List.objects.filter(board=board)
        print(f'Se crearon {len(list_names)} listas')
    else:
        print(f'Usando {len(lists)} listas existentes')

    # Crear tarjetas de ejemplo
    cards_data = [
        {
            'list': 'Por hacer',
            'title': 'Investigar nuevas tecnologías',
            'description': 'Buscar información sobre React, Vue y Angular para el próximo proyecto.',
            'due_date': timezone.now() + datetime.timedelta(days=7)
        },
        {
            'list': 'Por hacer',
            'title': 'Actualizar documentación',
            'description': 'La documentación del API necesita ser actualizada con los últimos cambios.',
            'due_date': timezone.now() + datetime.timedelta(days=3)
        },
        {
            'list': 'Por hacer',
            'title': 'Planificar reunión de equipo',
            'description': 'Coordinar una reunión para discutir la hoja de ruta del producto.',
            'due_date': timezone.now() + datetime.timedelta(days=1)
        },
        {
            'list': 'En progreso',
            'title': 'Corregir errores del sprint anterior',
            'description': 'Revisar los tickets de errores reportados y solucionarlos.',
            'due_date': timezone.now() - datetime.timedelta(days=1)
        },
        {
            'list': 'En progreso',
            'title': 'Implementar nueva funcionalidad',
            'description': 'Desarrollar la funcionalidad de búsqueda avanzada.',
            'due_date': timezone.now() + datetime.timedelta(days=2)
        },
        {
            'list': 'En revisión',
            'title': 'Revisar pull request #42',
            'description': 'Verificar cambios realizados en la rama feature/user-profiles.',
            'due_date': timezone.now()
        },
        {
            'list': 'Completado',
            'title': 'Actualizar dependencias',
            'description': 'Se actualizaron todas las dependencias a las últimas versiones estables.',
            'due_date': None
        },
    ]

    # Obtener las etiquetas
    labels = Label.objects.filter(board=board)
    if not labels:
        print('No hay etiquetas. Creando etiquetas por defecto.')
        label_data = [
            {'name': 'Verde', 'color': 'green'},
            {'name': 'Amarillo', 'color': 'yellow'},
            {'name': 'Naranja', 'color': 'orange'},
            {'name': 'Rojo', 'color': 'red'},
            {'name': 'Morado', 'color': 'purple'},
            {'name': 'Azul', 'color': 'blue'},
        ]
        for label in label_data:
            Label.objects.create(name=label['name'], color=label['color'], board=board)
        labels = Label.objects.filter(board=board)
        print(f'Se crearon {len(labels)} etiquetas')
    else:
        print(f'Usando {len(labels)} etiquetas existentes')

    # Crear las tarjetas
    created_cards = 0
    for i, card_data in enumerate(cards_data):
        list_obj = List.objects.filter(board=board, title=card_data['list']).first()
        if not list_obj:
            print(f'Lista {card_data["list"]} no encontrada. Saltando tarjeta.')
            continue
            
        card = Card.objects.create(
            title=card_data['title'],
            description=card_data['description'],
            list=list_obj,
            order=i,
            due_date=card_data['due_date']
        )
        
        # Asignar etiquetas aleatorias (entre 0 y 2 etiquetas por tarjeta)
        num_labels = random.randint(0, 2)
        if num_labels > 0:
            random_labels = random.sample(list(labels), min(num_labels, len(labels)))
            for label in random_labels:
                card.labels.add(label)
        
        created_cards += 1

    print(f'¡{created_cards} tarjetas creadas con éxito!')

if __name__ == "__main__":
    reset_cards() 