from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Task
from .forms import TaskForm, EditTaskForm

def index(request):
    newTaskForm = TaskForm()
    forms = []

    tasks = Task.objects.filter()
    for task in tasks:
        forms.append( EditTaskForm(instance=task) )
    return render(request, "tasks/index.html", {'newTaskForm': newTaskForm, 'forms': forms})

def saveTask(request):
    scrollTo = ""

    if request.method == 'POST':
        
        # New task
        if request.POST.get('task_id') == None:
            form = TaskForm( request.POST )
        
        # Editing existing task
        else:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, pk=task_id)
            form = EditTaskForm( request.POST, instance=task )

        if form.is_valid():
            task = form.save()

        scrollTo = f"#{task.id}"
    
    return HttpResponseRedirect( reverse('tasks:index') + scrollTo )

def deleteTask(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
    return HttpResponseRedirect( reverse('tasks:index') )

