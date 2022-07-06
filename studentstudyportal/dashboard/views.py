from doctest import Example
from email import message
from email.mime import audio
from multiprocessing import context
from operator import truediv
from pickle import TRUE
import re
from turtle import title
from django.contrib import messages
from django.shortcuts import redirect, render
import wikipedia
from django.contrib.auth.decorators import login_required


from . forms import *
from youtubesearchpython import VideosSearch
import requests 


# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"NOTES ADDED SUCUSSEFULLY")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user) #to display database table in html page
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
""""
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
                finished=False
            homeworks = Homework(
                user = request.user,
                subject =request.POST['subject'],
                title =request.POST['title'],
                description =request.POST['description'],
                due =request.POST['due'],
                is_finished =finished
            )
            homework.save()
            message.success(request,f"HOMEWORK ADDED FROM{request.user.username}")
    else:
         form = HomeworkForm() #cretaing object of HomeworkForm

    homework = Homework.objects.filter(user=request.user) #to dispaly homework table in homework.html file
    if len(homework) == 0: #TO CHECK WHETHER ALL HOMEWORK ARE COMPLETED and to dispaly all home works are done in its htmlfile
            homework_done=True
    else:
        homework_done=False
    context = {'homeworks':homework,'homeworks_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)

#if we click checkbox in homework.html then it should update
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return  redirect('homework')
    """

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text=request.POST['text']
        video = VideosSearch(text,limit=10) #func to search from utube
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc=""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:

        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == 'POST':        #when we clcih on create button in todo.html it should save indatabse
        form  = TodoForm(request.POST)   
        try:
            finished = request.POST["is_finished"]
            if finished == 'on':
                finished = True
            else:
                finished = False
        except:
            finished = False
        todos = Todo(           #creating Todos objects
            user = request.user,
            title = request.POST['title'],
            is_finished = finished

        )   
        todos.save()
    else:                             
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False

    context={
        'todos':todo,
        'form':form,
        'todos_done':todos_done

    }
    return render(request,"dashboard/todo.html",context)
@login_required
def update_todo(request,pk=None): #when u click on section on todo.html u have to udate whether it is finished or not
    todo = Todo.objects.get(id=pk)   #so we get the databse informatuon on that particulat primary key row
    if todo.is_finished ==True:
        todo.is_finished =False
    else:
        todo.is_finished = True
    todo.save() #update the database
    return redirect('todo')
@login_required
def delete_todo(request,pk=None):  #to delete a record in db
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text=request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text #Books google API
        r = requests.get(url)   #execute the url (pip install requests) 
        answer = r.json() #we get result in json object
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],  #this is the json object format
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'), 
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:

        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/books.html",context)

def dictinoary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST) #create a form
        text=request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text #Books dictionary API
        r = requests.get(url)   #execute the url (pip install requests) 
        answer = r.json() #we get result in json object
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition'] #to get 1st example
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonoetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                    'form':form,
                    'input':'',
                }
        return render(request,"dashboard/dictionary.html",context)
    else:
        form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,"dashboard/dictionary.html",context)


def wiki(request):
    if request.method == 'POST':
        text=request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
    
        context ={
        'form':form,
        'title':search.title,
        'link':search.url,
        'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form = DashboardForm()
    context={
        'form': form
    }
    return render(request,"dashboard/wiki.html",context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/33} yard'
                    context ={
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                    }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.45352} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20} pound'
                    context ={
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                    }


    else:    

        form = ConversionForm()
        context = {
        'form':form,
        'input':False
        }
    return render(request,"dashboard/conversion.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"ACCOUNTED CREATED FOR {username}!!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request,"dashboard/register.html",context)

@login_required
def profile(request):
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(todos)==0:
        todos_done = True
    else:
        todos_done = False
    context={
        'todos':todos,
        'todos_done':todos_done
    }
    return render(request,"dashboard/profile.html",context)