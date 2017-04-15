# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask_app.models import Profile
from faker import Factory

class Command(BaseCommand):
    args = "<--number number_users>\n" \
           "<-n number_users>"

    def add_arguments(self, parser):
        parser.add_argument("--number","-n",type=int,dest="number",
                            action="store",
                            help="Number of users",default=1)

    def handle(self, *args, **options):
        fake = Factory.create('ru_RU')
        number = options["number"]

        for i in range(number):
            profile = fake.simple_profile()
            user = User.objects.create_user(profile["username"],profile["mail"],make_password("qwerty123"))
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.is_active = True
            user.save()

            profile_user = Profile()
            profile_user.user = user
            profile_user.name = user.first_name + " " + user.last_name
            profile_user.save()
            self.stdout.write("Added %d user %s to database." % (profile_user.id, profile_user.name))




