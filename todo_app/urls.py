from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/complete/<int:todo_id>/', views.complete_todo, name='complete_todo'),
    path('todos/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
