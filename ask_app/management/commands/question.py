# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question,Profile
import random
from faker import Factory

class Command(BaseCommand):
    args = "<--number number_question\n>"

    def add_arguments(self, parser):
        parser.add_argument("--number","-n",type=int,dest="number",
                            action="store",
                            help="Number of question",default=0)

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')
        number = options["number"]
        profiles = Profile.objects.all()[1:]

        for i in range(number):
            question = Question()
            question.title = fake.sentence(nb_words=random.randint(10,20))
            question.text = fake.text(max_nb_chars=400)
            question.author = random.choice(profiles)
            question.save()
            self.stdout.write("Added question %d to database." % (question.id))




