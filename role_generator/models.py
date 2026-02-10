from django.db import models
from django.contrib import sessions
import random
import string


# Create your models here.


# create room model <i>
class Room(models.Model):
    code = models.CharField(max_length=4, unique=True, db_index=True)
    host = models.CharField(max_length=32)
    # users = models.ManyToManyField(to=sessions, blank=True)

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

# create user model <c>
class RoomParticipant(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="participants")    # change CASCADE if users are saved
    session = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now=True)