from django.http import HttpResponse
from .models import Room


def see_one_room(req, room_id):
    room = Room.objects.get(pk=room_id)
    return HttpResponse(f"{room}")


def see_all_rooms(req):
    rooms = Room.objects.all()
    return HttpResponse(rooms)
