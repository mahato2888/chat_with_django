from django.shortcuts import render, redirect, HttpResponse
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')

def room(request, room, username):
    username = username
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html',{

        'username': username,
        'room': room_details.name,
        'room_details': room_details,
    })

def checkview(request):
    room = request.POST['room_name'] 
    username = request.POST['username'] 


    if Room.objects.filter(name=room).exists():  # room name inputed exist
        return redirect('/'+room+'/'+username)
    else:
        new_room = Room.objects.create(name=room, username=username)
        new_room.save()
        return redirect('/'+room+'/'+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    #return HttpResponse("Hi, Message sent successfully")

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

class SingUp(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('signup')