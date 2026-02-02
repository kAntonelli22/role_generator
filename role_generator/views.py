from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Room
from django.shortcuts import redirect, get_object_or_404

def homepage(request):
    return render(request, 'role_generator/homepage.html')

def create_room(request):
    room = Room.create_room()
    return redirect('room', room_code=room.code)


@require_http_methods(["POST"])
def join_room(request):    
    room_code = request.POST.get('room_code')
    print(room_code)

    try:
        room = Room.objects.get(code=room_code)

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

    context = {
        'room': room,
        'room_code': room_code
    }
    return render(request, 'role_generator/room.html', context)