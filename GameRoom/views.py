from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import GameRoom, Player
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your views here.


def test(request):
    return render(request, 'GameRoom/test.html', {
    })


def menu(request):
    # Iegūstam izmetā lietotāja informāciju no sesijas (ja tā ir)
    removed_player_username = request.session.pop(
        'removed_player_username', None)
    removed_player_email = request.session.pop('removed_player_email', None)

    # Jūs varat padot informāciju no sesijas uz menu lapu izmantojot kontekstu
    return render(request, 'GameRoom/StartMenu.html', {
        'removed_player_username': removed_player_username,
        'removed_player_email': removed_player_email,
    })


@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        max_players = request.POST.get('max_players')

        if max_players is None or max_players == '':
            return render(request, 'GameRoom/CreateRoom.html', {'error': 'Player count is required.'})

        # Convert max_players to an integer
        max_players = int(max_players)

        is_private = request.POST.get('is_private', False) == 'on'
        password = request.POST.get('password')

        room = GameRoom.objects.create(
            code=room_code,
            max_players=max_players,
            is_private=is_private,
            password=password,
            created_by=request.user
        )

        player = Player.objects.create(
            user=request.user, room=room, is_owner=True)
        room.save()

        request.user.is_in_room = True
        request.user.save()

        return redirect('GameRoom:room', room_code=room.code)

    return render(request, 'GameRoom/CreateRoom.html')


def logout_view(request):
    logout(request)
    # Norādiet lapas nosaukumu, uz kuru vēlaties pāradresēt pēc atslēgšanās
    return redirect('home')


@login_required(login_url='login')
def room(request, room_code):
    try:
        room = GameRoom.objects.get(code=room_code)
    except GameRoom.DoesNotExist:
        raise Http404("Room does not exist")

    players = Player.objects.filter(room=room)

    return render(request, 'GameRoom/room.html', {'room': room, 'players': players})


@login_required(login_url='login')
def join_room(request):
    rooms = GameRoom.objects.all()

    if request.method == 'POST':
        room_code = request.POST.get('room_code')

        try:
            room = GameRoom.objects.get(code=room_code)

            # Pārbaude vai istaba ir privāta un vai ievadītā parole ir pareiza
            if room.is_private:
                entered_password = request.POST.get('password')
                if entered_password == room.password:
                    player = Player.objects.create(
                        user=request.user, room=room)
                    room.save()
                    return redirect('GameRoom:room', room_code=room_code)
                else:
                    return render(request, 'GameRoom/join_room.html', {'rooms': rooms, 'error': 'Incorrect password'})

            else:
                player = Player.objects.create(user=request.user, room=room)
                room.save()
                return redirect('GameRoom:room', room_code=room_code)

        except GameRoom.DoesNotExist:
            return render(request, 'GameRoom/join_room.html', {'rooms': rooms, 'error': 'Room does not exist'})

    return render(request, 'GameRoom/join_room.html', {'rooms': rooms})


@login_required(login_url='login')
def leave_room(request):
    try:
        player = Player.objects.get(user=request.user)
        room = player.room
        if player.is_owner:
            new_owner = Player.objects.filter(
                room=player.room).exclude(id=player.id).first()
            if new_owner:
                new_owner.is_owner = True
                new_owner.save()

        player.delete()

        room.save()

        return redirect('menu')  # Aizvietojiet ar atbilstošo URL
    except Player.DoesNotExist:
        # Ja spēlētājs nav atrasts, vienkārši atgriežamies uz menu lapu
        return redirect('menu')
