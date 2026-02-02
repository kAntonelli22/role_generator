from django.db import models
import random
import string


# Create your models here.


# create room model <i>
class Room(models.Model):
    code = models.CharField(max_length=4, unique=True, db_index=True)
    # users = models.ManyToManyField(max_length=255)

    def __str__(self):
        return self.code
    
    @staticmethod
    def generate_room_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if not Room.objects.filter(code=code).exists():
                return code
    
    @classmethod
    def create_room(cls):
        code = cls.generate_room_code()
        room = cls.objects.create(code=code)
        return room

# create card model <i>
class Card(models.Model):
    pass

# create user model <i>
class User(models.Model):
    name = models.CharField(max_length=255)