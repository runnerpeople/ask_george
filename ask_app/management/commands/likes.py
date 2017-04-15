# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask_app.models import Question,QuestionLike, Answer, AnswerLike, Profile
import random

class Command(BaseCommand):
    args = "<-num_ans number_answer -num_ques number_question \n>"

    def add_arguments(self, parser):
        parser.add_argument("-num_ans",type=int,dest="num_ans",
                            action="store",
                            help="Number of likes for an answer",default=0)
        parser.add_argument("-num_ques", type=int, dest="num_ques",
                            action="store",
                            help="Number of likes for a question", default=0)

    def handle(self, *args, **options):
        number_answers = options['num_ans']
        number_questions = options['num_ques']

        profiles = Profile.objects.all()[1:]
        questions = Question.objects.all()

        for q in questions:
            self.stdout.write("Added like question %d to database." % (q.id))
            for i in range(number_questions):
                QuestionLike.objects.create_or_update(q,author=random.choice(profiles),value=random.choice([-1,1]))

        answers = Answer.objects.all()
        for a in answers:
            self.stdout.write("Added like answer %d to database." % (a.id))
            for i in range(number_answers):
                AnswerLike.objects.create_or_update(a, author=random.choice(profiles), value=random.choice([-1, 1]))

