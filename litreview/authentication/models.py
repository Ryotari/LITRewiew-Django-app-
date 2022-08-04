#SuperUser: Username='SuperUser', Password='Superpass1'
#User1: Username='Username1', Password='password5224'
#User2: Username='Username2', Password='pass5224'
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	pass
