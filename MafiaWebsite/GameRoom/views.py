from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import GameRoom, Player, Chat
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your views here.


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
    hat_messages = room.chat_set.all().order_by('created_at')

    return render(request, 'GameRoom/room.html', {'room': room, 'players': players})


def check_and_delete_room(request, room_code):
    # Atrodam istabu pēc tās koda
    room = get_object_or_404(GameRoom, code=room_code)

    # Atrodam visus spēlētājus, kas atrodas šajā istabā
    players_in_room = Player.objects.filter(room=room)

    # Atjaunojam player_count atbilstoši spēlētāju skaitam
    room.player_count = players_in_room.count()
    room.save()

    return JsonResponse({'status': 'active'})


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
def change_owner(request, room_code, player_id):
    print("Pieprasījuma lietotājs:", request.user)

    # Iegūst `request.user` id
    request_user_id = request.user.id
    print(request_user_id)

    owner_player = get_object_or_404(
        Player, user_id=request_user_id, room__code=room_code)

    # Pārbauda, vai pašreizējais lietotājs ir istabas īpašnieks (owners)
    current_player = get_object_or_404(
        Player, id=player_id, room__code=room_code)
    print("Pašreizējais spēlētājs:", current_player)

    if owner_player.is_owner:
        players = Player.objects.filter(room__code=room_code)
        print("Visi spēlētāji istabā:", players)

        # Nomaina istabas īpašnieka statusu
        current_player.is_owner = True
        current_player.save()
        owner_player.is_owner = False
        owner_player.save()

    else:
        print("Piekļuve liegta. Pašreizējais spēlētājs nevar mainīt īpašnieku.")

    return redirect('GameRoom:room', room_code=room_code)


def get_rooms_api(request):
    rooms = GameRoom.objects.all()  # Vajadzētu iegūt istabu datus pēc vajadzības
    room_data = [{'code': room.code} for room in rooms]
    return JsonResponse(room_data, safe=False)


@csrf_exempt
def check_user_status(request):
    if request.method == 'POST':
        # Šeit iegūstiet lietotāja statusu vai veiciet nepieciešamās darbības
        response_data = {'message': 'User status checked successfully'}
        return JsonResponse(response_data)
        room.save()
    else:
        # Ja pieprasījums nav POST metode, atgriez atbilstošu kļūdas atbildi
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)


@login_required(login_url='login')
def get_room_data(request):
    rooms = GameRoom.objects.all()
    room_data = []

    for room in rooms:
        # Pārbaudiet, vai šajā istabā nav neviena spēlētāja
        if room.player_count == 0:
            room.delete()
        else:
            room_data.append({
                'code': room.code,
                'player_count': room.player_count,
                'max_players': room.max_players,
                'is_private': room.is_private
            })

    return JsonResponse({'room_data': room_data})


def room_view(request, room_code):
    room = GameRoom.objects.get(code=room_code)
    players = Player.objects.filter(room=room)
    context = {
        'room': room,
        'players': players,
    }
    return render(request, 'room.html', context)


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


@login_required(login_url='login')
def remove_player(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
        room = player.room

        # Pārbauda, vai pieprasījuma iesniedzējs ir istabas īpašnieks
        if room.created_by == request.user:
            player_username = player.user.username
            player.delete()
            room.save()

            # Paziņojiet par izmesto spēlētāju, izmantojot WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"room_{room.code}",
                {
                    'type': 'kick_player',
                    'message': f'Player {player_username} has been kicked from the room.'
                }
            )

            return redirect(reverse('GameRoom:room', kwargs={'room_code': room.code}))

    except Player.DoesNotExist:
        pass

    raise Http404(
        "Player not found or you don't have permission to remove the player.")
