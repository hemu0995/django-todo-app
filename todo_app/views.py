from django.shortcuts import render, redirect
from .models import TodoItem

def index(request):
    return render(request, 'index.html')

def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            TodoItem.objects.create(title=title)
        return redirect('todo_list')
    
    todos = TodoItem.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def complete_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

def delete_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.delete()
    return redirect('todo_list')
