from django.shortcuts import render
from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.shortcuts import render,redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import json

def home(request):
    return render(request,'dashboard/index.html')
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f"Note added successfully by {request.user.username}") 
    else:
        form = NotesForm()
    notes =Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
     model = Notes



def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished    
            )
            homeworks.save()
            messages.success(request,f"Homework adeed from {request.user.username}!!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    context ={'homeworks': homework,
              'homeworks_done':homework_done, 
              'form':form}
    return render(request, 'dashboard/homework.html', context)

def update_homework(request,pk=None):
    homework =Homework.object.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished == False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")









def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=1)
        result_list=[]
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
        context = {
            'form':form,
            'result':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)















def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added From{request.user.username}")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'todos':todo,
        'form':todo,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)


def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

# def books(request):
#     form = DashboardForm()
#     context = {'form':form}
#     return render(request,"dashboard/books.html",context)






# def books(request):
#     if request.method == "POST":
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         url = "https://www.googleapis.com/books/v1/volumes?q=" + text
#         r = requests.get(url)

#         if r.status_code == 200:
#             try:
#                 answer = r.json()
#                 result_list = []

#                 for item in answer.get('items', [])[:10]:
#                     volume_info = item.get('volumeInfo', {})
#                     result_dict = {
#                         'title': volume_info.get('title', ''),
#                         'subtitle': volume_info.get('subtitle', ''),
#                         'description': volume_info.get('description', ''),
#                         'count': volume_info.get('pageCount', ''),
#                         'categories': volume_info.get('categories', []),
#                         'rating': volume_info.get('averageRating', ''),
#                         'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
#                         'preview': volume_info.get('previewLink', ''),
#                     }
#                     result_list.append(result_dict)

#                 context = {
#                     'form': form,
#                     'result': result_list
#                 }
#                 return render(request, 'dashboard/books.html', context)

#             except json.decoder.JSONDecodeError as e:
#                 print("Error decoding JSON:", e)
#         else:
#             print("API Request failed with status code:", r.status_code)

#     else:
#         form = DashboardForm()
#         context = {'form': form}
#         return render(request, "dashboard/books.html", context)
