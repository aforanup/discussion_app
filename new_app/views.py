from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomCreateForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    topics = Topic.objects.all()
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query)
    )
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms.count()}
    return render(request, 'new_app/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'new_app/room.html', {'room': room})


@login_required(login_url='login')
def create(request):
    form = RoomCreateForm
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'new_app/create.html', {'form': form})


@login_required(login_url='login')
def update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomCreateForm(instance=room)

    if request.user != room.user:
        return HttpResponse('You are not allowed to edit this room!!')

    if request.method == 'POST':
        form = RoomCreateForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'new_app/create.html', {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.user:
        return HttpResponse('You are not allowed to delete this room!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'new_app/delete.html', {'obj': room})


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'Username doesnot exist.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password doesnot match')
    return render(request, 'new_app/login_registration.html', {'page': page})


def registerUser(request):
    page = 'register'
    return render(request, 'new_app/login_registration.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')
