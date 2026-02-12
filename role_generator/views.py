from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Room
from .models import RoomParticipant
from django.shortcuts import redirect, get_object_or_404
import random
import datetime
from django.utils import timezone
from datetime import timedelta

def homepage(request):
    return render(request, 'role_generator/homepage.html')

def create_room(request):
    room = Room.create_room()

    host = RoomParticipant.objects.create(
            name="Host",
            room=room,
            session=request.session.session_key
        )

    if not request.session.session_key:
        request.session.create()

    room.host = host.session
    room.save()

    return redirect('room', room_code=room.code)


@require_http_methods(["POST"])
def join_room(request):    
    room_code = request.POST.get('room_code')

    try:
        room = Room.objects.get(code=room_code)

        if not request.session.session_key:
            request.session.create()
        
        participant = RoomParticipant.objects.create(
            name="New User",
            room=room,
            session=request.session.session_key
        )

        return JsonResponse({
            'success': True,
            'redirect_url': f'/room/{room_code}/'
        })
    
    except Room.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Invalid room code'
        })

def room(request, room_code):
    room = get_object_or_404(Room, code=room_code)

    participants_data = []
    for p in room.participants.all():
        participants_data.append({
            'name': p.name,
            'is_host': p.session == room.host,
            'is_current_user': p.session == request.session.session_key
        })

    context = {
        'room': room,
        'room_code': room_code,
        'participants': participants_data
    }
    return render(request, 'role_generator/room.html', context)


def update_user(request, room_code):
    room = get_object_or_404(Room, code=room_code)
    user = get_object_or_404(RoomParticipant, session=request.session.session_key, room=room)
    user.last_seen = timezone.now()
    user.save()

    if random.random() < 0.1:
        print("Random user cleanup called")
        cutoff = timezone.now() - timedelta(minutes=1)
        RoomParticipant.objects.filter(last_seen__lt=cutoff).delete()
        Room.objects.filter(participants__isnull=True).delete()

    participants_data = []
    for p in room.participants.all():
        participants_data.append({
            'name': p.name,
            'is_host': p.session == room.host,
            'is_current_user': p.session == request.session.session_key
        })

    return JsonResponse({'participants': participants_data})