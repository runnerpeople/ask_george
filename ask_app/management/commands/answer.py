# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question,Answer,Profile
import random
from faker import Factory

class Command(BaseCommand):
    args = "<--number number_answer\n>"

    def add_arguments(self, parser):
        parser.add_argument("--number","-n",type=int,dest="number",
                            action="store",
                            help="Number of question",default=0)

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')
        number = options["number"]
        profiles = Profile.objects.all()[1:]
        question = Question.objects.all()
        for q in question:
            for i in range(number):
                answer = Answer()
                answer.text = fake.text(max_nb_chars=400)
                answer.author = random.choice(profiles)
                answer.question = q
                answer.save()
                self.stdout.write("Added answer %d to database."
                                  "Question %d" % (answer.id,q.id))




