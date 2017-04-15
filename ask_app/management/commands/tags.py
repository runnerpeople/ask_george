# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from ask_app.models import Tag,Question
import random
from faker import Factory

class Command(BaseCommand):
    args = "<--number number_tags>\n" \
           "<-n number_tags>"

    def add_arguments(self, parser):
        parser.add_argument("--number","-n",type=int,dest="number",
                            action="store",
                            help="Number of tags",default=1)

    def handle(self, *args, **options):
        fake = Factory.create('en_EN')
        number = options["number"]

        for i in range(number):
            tag = Tag()
            tag.name = fake.sentence(nb_words=1)
            tag.save()

        question = Question.objects.all()
        tag = Tag.objects.all()

        for q in question:
            number_tag = random.randint(1,3)
            if len(tag) < number_tag:
                for i in range(0,number_tag - len(tag)):
                    tag = random.choice(tag)
                    if tag not in question.tags.all():
                        question.tags.add(tag)




