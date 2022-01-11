from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomCreateForm
from django.db.models import Q


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


def create(request):
    form = RoomCreateForm
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'new_app/create.html', {'form': form})


def update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomCreateForm(instance=room)

    if request.method == 'POST':
        form = RoomCreateForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'new_app/create.html', {'form': form})


def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'new_app/delete.html', {'obj': room})


def loginUser(request):
    pass


def logoutUser(request):
    pass
