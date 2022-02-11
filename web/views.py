from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User, Request, Project, Task
from hashlib import sha256, sha1
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
import datetime
import json

def index(request):
    return render(request, "index.html")

def login(request):
    try:
        login = request.session['login']
        if(login):
            del request.session['login']
            del request.session['role']
    finally:
        if request.method == "POST":
            login = request.POST.get("login")
            password = request.POST.get("password")
            message = ""
            try:
                user = User.objects.get(login=login)
                hash = sha256(password.encode('utf-8')).hexdigest()
                if(user.password == hash):
                    request.session['login'] = login
                    request.session['role'] = user.role
                    if(request.session['role'] == "manager"):
                        return HttpResponseRedirect('/cards')
                    if(request.session['role'] == "projectmanager"):
                        return HttpResponseRedirect('/projects')
                    if(request.session['role'] == "executor"):
                        return HttpResponseRedirect('/projects')
                else:
                    message = "Неверный логин или пароль"
                    return render(request, "login.html", {"message": message})
            except User.DoesNotExist:
                message = "Неверный логин или пароль"
                return render(request, "login.html", {"message": message})
        else:
            return render(request, "login.html")
def cards(request):
    try:
        login = request.session['login']
        if(login):
            if(request.session['role'] == "manager"):
                requests = list(Request.objects.filter(status='created'))
                rows = []
                for i in range(len(requests)):
                    col = []
                    if(i % 2 == 0):
                        if(i+1 < len(requests)):
                            col.append(requests[i])
                            col.append(requests[i+1])
                            rows.append(col)
                        if(i+1 == len(requests)):
                                col.append(requests[i])
                                rows.append(col)
                return render(request, "cards.html", {"rows":rows})
            else:
                raise Http404()
    except KeyError:
        raise Http404()
def card(request, cardId):
    try:
        login = request.session['login']
        if(login):
            if(request.session['role'] == "manager"):
                if request.method == "POST":
                    card = Request.objects.get(id=cardId)
                    card.status = "accepted"
                    card.save()
                    description = request.POST.get("description")
                    deadline = request.POST.get("deadline")
                    deadline = str(deadline).split("/")
                    project  = Project()
                    project.creator = User.objects.get(login=login)
                    project.description = description
                    project.request = card
                    project.status = "created"
                    project.deadline = datetime.date(int(deadline[2]), int(deadline[1]), int(deadline[0]))
                    project.creationDate =  datetime.datetime.now().date()
                    project.save()
                    return HttpResponseRedirect('/cards')
                else:
                    card = Request.objects.get(id=cardId)
                    return render(request, "card.html", {"card":card})
            else:
                raise Http404()
    except KeyError:
        raise Http404()

def reject(request, id):
        try:
            login = request.session['login']
            if(login):
                if(request.session['role'] == "manager"):
                    card = Request.objects.get(id=id)
                    card.status = "rejected"
                    card.save()
                    return HttpResponseRedirect('/cards')
                else:
                    raise Http404()
        except KeyError:
            raise Http404()

def newrequest(request):
    if request.method == "POST":
        creator = request.POST.get("creator")
        description = request.POST.get("description")
        phoneNumber = request.POST.get("phoneNumber")
        email = request.POST.get("email")
        additional = request.POST.get("additional")

        request  = Request()
        request.creator = creator
        request.description = description
        request.phoneNumber = phoneNumber
        request.email = email
        request.additional = additional
        request.status = "created"
        request.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, "newrequest.html")

def projectsForExecutor(login):
    user = User.objects.get(login=login)
    tasks = list(Task.objects.filter(executor_id=user.id))
    projects = []
    for task in tasks:
        project = task.project
        if project not in projects:
            projects.append(project)
    return projects
def projects(request):
    try:
        login = request.session['login']
        if(login):
            if(request.session['role'] == "projectmanager"):
                newcards = list(Project.objects.filter(status = 'created'))
                curcards = list(Project.objects.filter(status = 'inprocess'))
                cards = [*newcards, *curcards]
                rows = []
                for card in cards:
                    card.deadline = str(card.deadline.day) + "/" + str(card.deadline.month) + "/" + str(card.deadline.year)
                for i in range(len(cards)):
                    col = []
                    if(i % 2 == 0):
                        if(i+1 < len(cards)):
                            col.append(cards[i])
                            col.append(cards[i+1])
                            rows.append(col)
                        if(i+1 == len(cards)):
                                col.append(cards[i])
                                rows.append(col)
                return render(request, "projects.html", {"rows":rows})
            if(request.session['role'] == "executor"):
                cards = projectsForExecutor(login)
                rows = []
                for i in range(len(cards)):
                    col = []
                    if(i % 2 == 0):
                        if(i+1 < len(cards)):
                            col.append(cards[i])
                            col.append(cards[i+1])
                            rows.append(col)
                        if(i+1 == len(cards)):
                                col.append(cards[i])
                                rows.append(col)
                return render(request, "projects.html", {"rows":rows})
            else:
                raise Http404()
    except KeyError:
        raise Http404()

def checkExecutorForProject(login, projectid):
    projects = projectsForExecutor(login)
    for project in projects:
        if(project.id == projectid):
            return True
    return False
def project(request, id):
    try:
        login = request.session['login']
        if(login):
            if(request.session['role'] == "projectmanager"):
                if request.method == "POST" and request.POST.get("executor")!= "Исполнитель":

                    description = request.POST.get("description")
                    executor = User.objects.get(id=request.POST.get("executor"))
                    project = Project.objects.get(id=id)
                    try:
                        task = Task.objects.get(description=description, executor = executor, project=project)
                    except Task.DoesNotExist:
                        task = Task()
                        task.executor = executor
                        task.description = description
                        task.project = project
                        task.status = "todo"
                        task.deadline = datetime.datetime.now().date()
                        task.creationDate =  datetime.datetime.now().date()
                        task.save()

                        project.status = "inprocess"
                        project.save()

                    newtasks = list(Task.objects.filter(project_id=id).filter(status="todo"))
                    curtasks = list(Task.objects.filter(project_id=id).filter(status="inprocess"))
                    oldtasks = list(Task.objects.filter(project_id=id).filter(status="done"))
                    executors = list(User.objects.filter(role="executor"))

                    return render(request, "project.html", {"pm": True, "new":newtasks, "cur":curtasks, "old":oldtasks, "executors": executors})
                else:
                    newtasks = list(Task.objects.filter(project_id=id).filter(status="todo"))
                    curtasks = list(Task.objects.filter(project_id=id).filter(status="inprocess"))
                    oldtasks = list(Task.objects.filter(project_id=id).filter(status="done"))
                    executors = list(User.objects.filter(role="executor"))

                    return render(request, "project.html", {"pm": True,"new":newtasks, "cur":curtasks, "old":oldtasks, "executors": executors})
            if(request.session['role'] == "executor" and checkExecutorForProject(login,id)):
                newtasks = list(Task.objects.filter(project_id=id).filter(status="todo"))
                curtasks = list(Task.objects.filter(project_id=id).filter(status="inprocess"))
                oldtasks = list(Task.objects.filter(project_id=id).filter(status="done"))
                executors = list(User.objects.filter(role="executor"))

                return render(request, "project.html", {"pm": False, "new":newtasks, "cur":curtasks, "old":oldtasks, "executors": executors})

            else:
                raise Http404()
    except KeyError:
        raise Http404()

def checkProject(id):
    tasks = list(Task.objects.filter(project_id=id))
    for task in tasks:
        if(task.status == "todo" or task.status == "inprocess"):
            return False
    return True
@csrf_exempt
def updateTasks(request):
    if(request.method == 'POST'):
        body = json.loads(request.body)
        todo = body['backlog']
        inprocess = body['process']
        done = body['completed']

        if(todo != ""):
            todos = todo.split(",")
            for item in todos:
                task = Task.objects.get(id=item)
                if(task.status != "todo"):
                    task.status = "todo"
                    task.save()
        if(inprocess != ""):
            process = inprocess.split(",")
            for item in process:
                task = Task.objects.get(id=item)
                if(task.status != "inprocess"):
                    task.status = "inprocess"
                    task.save()
        if(done != ""):
            dones = done.split(",")
            projId = 0
            for item in dones:
                task = Task.objects.get(id=item)
                if(task.status != "done"):
                    projId = task.project_id
                    task.status = "done"
                    task.save()
            if(checkProject(projId)):
                project = Project.objects.get(id=projId)
                project.status = "done"
                project.save()
def getStatistic():
    arr = []
    arr.append(len(list(Request.objects.filter(status="accepted"))))
    arr.append(len(list(Request.objects.filter(status="rejected"))))
    arr.append(len(list(Project.objects.filter(status="done"))))
    arr.append(len(list(Project.objects.all()))-arr[2])
    arr.append(len(list(Task.objects.filter(status="todo"))))
    arr.append(len(list(Task.objects.filter(status="inprocess"))))
    arr.append(len(list(Task.objects.filter(status="done"))))
    arr.append(len(list(Request.objects.filter(status="created"))))
    return arr
def statistic(request):
    arr = getStatistic()
    return render(request, "statistic.html", {"arr": arr})
