from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def parse_args(request):
    response = "<p> WSGI script by George Ivanov (Django) </p>" \
               "<form method='POST'>"\
               "<p><input type='text' name='str'></p>" \
               "<p><input type='submit' value='Send!'></p>" \
               "</form>"
    if request.method=='GET':
        if request.GET=={}:
            response += "No data received"
        else:
            for key,value in request.GET.iteritems():
                if len(value) == 1:
                    response += "%s = %s <br>" % (key, value[0])
                else:
                    response += "%s = %s <br>" % (key, value)
    elif request.method=='POST':
        response += "<h3> <p> Post data: </p> </h3>"
        response += "Value = %s <br>" % (request.POST['str'])
    return HttpResponse(response,content_type="text/html",status=200)
