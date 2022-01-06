from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from datetime import date, datetime

from .models import Task
from .forms import TaskForm, EditTaskForm

def index(request):

    newTaskForm = TaskForm()
    forms = []

    # User authenticated, so get saved tasks
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    
    # User isn't authenticated, so get tasks from session
    else:
        tasks = []

        if request.session.get('tasks', False):
            serializedTasks = request.session.get('tasks', [])
            for task_id in serializedTasks.keys():
                description = serializedTasks[task_id]['description']
                dateLimit = None
                if serializedTasks[task_id]['dateLimit'] != '':
                    dateLimit = datetime.strptime(serializedTasks[task_id]['dateLimit'], "%d/%m/%Y")
                concluded = serializedTasks[task_id].get('concluded', False)

                task = Task(description=description, dateLimit=dateLimit, concluded=concluded)
                task.id = task_id
                tasks.append( task )
        else:
            request.session['tasks'] = {}
            request.session['last_id'] = 0

    for task in tasks:
        forms.append( EditTaskForm(instance=task) )
    return render(request, "tasks/index.html", {'newTaskForm': newTaskForm, 'forms': forms})

def saveTask(request):
    scrollTo = ""

    if request.method == 'POST':
        
        if request.user.is_authenticated:
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
                task.user = request.user
                task.save()
                scrollTo = f"#{task.id}"
        else:
            # New task
            if request.POST.get('task_id') == None:
                form = TaskForm( request.POST )
                task_id = request.session['last_id'] + 1
                request.session['last_id'] = task_id
            # Edit task
            else:
                form = EditTaskForm( request.POST )
                task_id = request.POST.get('task_id')
                
            if form.is_valid():
                print(request.session.get('tasks'))
                description = form.cleaned_data['description']
                dateLimit = ''
                if form.cleaned_data.get('dateLimit', False):
                    date = form.cleaned_data['dateLimit']
                    dateLimit = date.strftime("%d/%m/%Y")
                concluded = form.cleaned_data.get('concluded',False)
                request.session['tasks'][task_id] = {
                    'description': description,
                    'dateLimit': dateLimit,
                    'concluded': concluded
                }

    return HttpResponseRedirect( reverse('tasks:index') + scrollTo )

def deleteTask(request):
    if request.method == "POST":
        task_id = int(request.POST['task_id'])

        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=task_id)
            task.delete()
        else:
            tasks = request.session.get('tasks')
            tasks.pop(task_id)
            request.session['tasks'] = tasks
    return HttpResponseRedirect( reverse('tasks:index') )

def react(request):
    tasks = Task.objects.all()
    return render(request, "tasks/index_react.html", {'tasks': tasks})
