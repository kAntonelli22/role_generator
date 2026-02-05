from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Room
from .models import RoomParticipant
from django.shortcuts import redirect, get_object_or_404

def homepage(request):
    return render(request, 'role_generator/homepage.html')

def create_room(request):
    room = Room.create_room()

    if not request.session.session_key:
        request.session.create()

    room.host = request.session.session_key
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
        print(p.name)
        participants_data.append({
            'name': p.name,
            'is_host': p.session == room.host,
            'is_current_user': p.session == request.session.session_key
        })
        print("participant: ", p.name, "\tis host? ", p.session == room.host, "\tis current user? ", p.session == request.session.session_key)

    context = {
        'room': room,
        'room_code': room_code,
        'participants': participants_data
    }
    return render(request, 'role_generator/room.html', context)