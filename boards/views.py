from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, List, Card, Label
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

def board_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    lists = board.lists.all()
    now = timezone.now()
    return render(request, 'boards/board_detail.html', {'board': board, 'lists': lists, 'now': now})

def create_board(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        board = Board.objects.create(
            title=title,
            description=description,
            owner_id=1  # Asignamos un ID por defecto
        )
        # Crear etiquetas por defecto
        default_labels = [
            {'name': 'Verde', 'color': 'green'},
            {'name': 'Amarillo', 'color': 'yellow'},
            {'name': 'Naranja', 'color': 'orange'},
            {'name': 'Rojo', 'color': 'red'},
            {'name': 'Morado', 'color': 'purple'},
            {'name': 'Azul', 'color': 'blue'},
        ]
        for label in default_labels:
            Label.objects.create(
                name=label['name'],
                color=label['color'],
                board=board
            )
        return redirect('board_detail', board_id=board.id)
    return render(request, 'boards/create_board.html')

def create_list(request, board_id):
    if request.method == 'POST':
        board = get_object_or_404(Board, id=board_id)
        title = request.POST.get('title')
        List.objects.create(
            title=title,
            board=board,
            order=board.lists.count()
        )
        return redirect('board_detail', board_id=board_id)
    return redirect('board_detail', board_id=board_id)

def create_card(request, list_id):
    if request.method == 'POST':
        list_obj = get_object_or_404(List, id=list_id)
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date_str = request.POST.get('due_date', '')
        
        due_date = None
        if due_date_str:
            try:
                due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
                due_date = timezone.make_aware(due_date)
            except ValueError:
                pass
        
        Card.objects.create(
            title=title,
            description=description,
            list=list_obj,
            due_date=due_date,
            order=list_obj.cards.count()
        )
        return redirect('board_detail', board_id=list_obj.board.id)
    return redirect('board_detail', board_id=list_obj.board.id)

def update_card_order(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        new_list_id = request.POST.get('new_list_id')
        new_position = request.POST.get('new_position')
        
        card = get_object_or_404(Card, id=card_id)
        new_list = get_object_or_404(List, id=new_list_id)
        
        # Actualizar la lista y posición de la tarjeta
        card.list = new_list
        card.order = new_position
        card.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    board_id = card.list.board.id
    card.delete()
    return redirect('board_detail', board_id=board_id)

def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return redirect('board_list')
