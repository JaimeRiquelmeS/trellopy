from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/create/', views.create_board, name='create_board'),
    path('board/<int:board_id>/list/create/', views.create_list, name='create_list'),
    path('list/<int:list_id>/card/create/', views.create_card, name='create_card'),
    path('card/update-order/', views.update_card_order, name='update_card_order'),
    path('card/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path('board/<int:board_id>/delete/', views.delete_board, name='delete_board'),
] 