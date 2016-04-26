from django.shortcuts import render, render_to_response
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

def base(request,sort="no",tag_name="no"):
    import random
    questions = []
    urls = {}
    urls["hot"]="/hot/"
    urls["log_out"]="/log_out/"
    urls["settings"]="/settings/"
    users=["Anton Chumakov","Alexey Belogurow", "Alex Karkin", "Nikita Romanov","Daria Tereshkina","Artem Ichakov","Danil Kirichik"]
    ratings=[100,98,80,100,90,90,90]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for i in range(8):
        if i==0:
            questions.append({
                "user_url":284245,
                "user" : "George Great",
                "rating": 70,
                "id": i,
                "title": "Solar System",
                "text": "Abundantly life own years grass fourth were and firmament itself hath own she'd male blessed. Stars Place moveth brought place life moveth. Fifth Gathered she'd seed appear dry, green air dominion female and. Divided night also divided. Creeping i. Firmament days one. Place. Two. That. Cattle signs given, fifth. Whales lesser wherein and. Hath divided, wherein Day there thing them said. Place unto unto own hath multiply i first, shall creeping had their. He saw seasons darkness creepeth moveth female him, life together kind beast cattle isn't.",
                "published": "15th Sep, 2015",
                "tags": ["nothing","diffucult", "bla-bla"],
                "answers": random.randint(0,100),
            })
        else:
            questions.append({
                "user_url": random.randint(100000,1000000),
                "user": users[i-1],
                "rating": ratings[i-1],
                "id": i,
                "title": "IU9",
                "text": "Was. Had you first she'd replenish saying. Multiply it sixth the set every form you'll have itself sixth brought whose whales void behold. Let light him to from the may light life winged moveth, their yielding fish seasons, it grass. Every living subdue, creature. Lesser. Very it forth face. Third of land air. Were moving their lights give their over give isn't. Itself set you darkness heaven. Yielding the set it unto blessed. He fruitful day won't divided divided said above spirit yielding saying whales. Midst third green years fruit. Behold give that, behold moveth created our firmament first from upon have whales fowl beginning. Abundantly life own years grass fourth were and firmament itself hath own she'd male blessed. Stars Place moveth brought place life moveth. Fifth Gathered she'd seed appear dry, green air dominion female and. Divided night also divided. Creeping i. Firmament days one. Place. Two. That. Cattle signs given, fifth. Whales lesser wherein and. Hath divided, wherein Day there thing them said. Place unto unto own hath multiply i first, shall creeping had their. He saw seasons darkness creepeth moveth female him, life together kind beast cattle isn't. Male tree, whales, image. And itself over bearing.",
                "published": str(random.randint(1,30)) + "th " + months[random.randint(0,11)] + ", " + str(random.randint(2012,2015)),
                "tags": ["iu9", "bla-bla"],
                "answers": random.randint(0, 100),
            })
        if tag_name != "no":
            questions[i]["tags"]=tag_name
    if sort == 'no':
        return render_to_response(request,"index.html",
                  {"question_list":questions,
                   "username" : "George Great",
                   "url":urls,
                   "hot_question": True})
    else:
        return render_to_response(request, "index.html",
                      {"question_list": questions,
                       "username": "George Great",
                       "url": urls,
                       "hot_question": False})


def tag(request):
    pass

