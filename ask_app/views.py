from django.shortcuts import render, render_to_response
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from paginator import Paginator
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout

def error_page(request):
    return render(request,"404.html")

@csrf_exempt
def parse_args(request):
    response = "<p> WSGI script by George Ivanov (Django) </p>" \
               "<form method='POST'>"\
               "<p><input type='text' name='str'></p>" \
               "<p><input type='submit' value='Send!'></p>" \
               "</form>"
    if request.method == 'GET':
        if request.GET:
            response += "No data received"
        else:
            for key,value in request.GET.iteritems():
                if len(value) == 1:
                    response += "%s = %s <br>" % (key, value[0])
                else:
                    response += "%s = %s <br>" % (key, value)
    elif request.method == 'POST':
        response += "<h3> <p> Post data: </p> </h3>"
        response += "Value = %s <br>" % (request.POST['str'])
    return HttpResponse(response,content_type="text/html",status=200)

def base(request,page,sort="no",tag="no"):
    questions = ""
    if sort != "no":
        questions = Question.objects.best()
    else:
        questions = Question.objects.all()
    if tag != "no":
        try:
            hash_tag = Tag.objects.find(tag)
        except Tag.DoesNotExist:
            return error_page(request)

        questions = Question.objects.tag(tag)
    questions_shown = paginate(questions,request)
    if tag != "no":
        return render(request, "index.html",
                                  {"question_list": questions_shown,
                                   "username": "George Great",
                                   "tag_block": True})
    if sort == 'no':
        return render(request,"index.html",
                  {"question_list":questions_shown,
                   "username" : "George Great",
                   "hot_question": True,
                   "tag_block": False})
    else:
        return render(request, "index.html",
                      {"question_list": questions_shown,
                       "username": "George Great",
                       "tag_block": False})


def question(request,question_id=0):
    question_ = ""
    try:
        question_ = Question.objects.get(pk=question_id)
        answers = Answer.objects.get_question(question_)
    except Question.DoesNotExist:
        return error_page(request)
    return render(request, "question.html",
                  {"question": question_,
                   "answer_list": answers,
                   "username": "George Great"})

def ask(request):
    return render(request,"ask.html",
                  {"username": "George Great"})

def login(request):
    return render(request, "login.html")

def sign_up(request):
    return render(request, "sign_up.html")



def paginate(objects_list,request):
    paginator = Paginator(objects_list,5)
    page = request.GET.get('page')
    contacts = paginator.page(page)
    return contacts

