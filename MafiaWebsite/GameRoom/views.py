from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import GameRoom, Player, Chat
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def menu(request):
    # Iegūstam izmetā lietotāja informāciju no sesijas (ja tā ir)
    removed_player_username = request.session.pop('removed_player_username', None)
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
            code = room_code,
            max_players = max_players,
            is_private = is_private,
            password = password,
            created_by = request.user
        )

        player = Player.objects.create(user=request.user, room=room, is_owner=True)
        room.player_count += 1
        room.save()

        request.user.is_in_room = True
        request.user.save()


        return redirect('GameRoom:room', room_code=room.code)

    return render(request, 'GameRoom/CreateRoom.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # Norādiet lapas nosaukumu, uz kuru vēlaties pāradresēt pēc atslēgšanās


@login_required(login_url='login')
def room(request, room_code):
    try:
        room = GameRoom.objects.get(code=room_code)
    except GameRoom.DoesNotExist:
        raise Http404("Room does not exist")

    players = Player.objects.filter(room=room)
    hat_messages = room.chat_set.all().order_by('created_at')

    return render(request, 'GameRoom/room.html', {'room': room, 'players': players})


def send_message(request, room_code):
    if request.method == 'POST':
        message = request.POST.get('message')

        # Ievietojiet nepieciešamās darbības, lai saglabātu ziņu datubāzē vai apstrādātu to
        try:
            room = GameRoom.objects.get(code=room_code)
        except GameRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found'})

        # Izveidojam jaunu čatas ierakstu
        chat_message = Chat.objects.create(room=room, sender=request.user, message=message)

        # Atgriežam veiksmes atbildi kā JSON
        return JsonResponse({'success': True})

    # Apstrādā gadījumu, ja saņemts GET pieprasījums
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def fetch_messages(request, room_code):
    if request.method == 'GET':
        # Atgriež JSON ar jaunākajām ziņām, kas ir saistītas ar šo istabu (GameRoom)
        try:
            room = GameRoom.objects.get(code=room_code)
            chat_messages = Chat.objects.filter(room=room).order_by('-created_at')[:10]

            messages = []
            for message in chat_messages:
                messages.append({
                    'sender': message.sender.username,
                    'message': message.message,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })

            return JsonResponse({'messages': messages})
        except GameRoom.DoesNotExist:
            return JsonResponse({'error': 'GameRoom does not exist'})

    # Apstrādā gadījumu, ja saņemts POST pieprasījums
    return JsonResponse({'error': 'Invalid request method'})



def check_and_delete_room(request, room_code):
    # Atrodam istabu pēc tās koda
    room = get_object_or_404(GameRoom, code=room_code)

    # Atrodam visus spēlētājus, kas atrodas šajā istabā
    players_in_room = Player.objects.filter(room=room)

    # Atjaunojam player_count atbilstoši spēlētāju skaitam
    room.player_count = players_in_room.count()
    room.save()

    # Ja vairs nav cilvēku istabā, izdzēšam istabu
    if room.player_count == 0:
        room.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'status': 'active'})

@login_required(login_url='login')
def join_room(request):
    rooms = GameRoom.objects.all()

    if request.method == 'POST':
        room_code = request.POST.get('real_code')
        password = request.POST.get('password')

        try:
            room = GameRoom.objects.get(code=room_code)

            if room.is_private and password != room.password:
                return JsonResponse({'success': False, 'error': 'Invalid password'})

            if room.player_count < room.max_players:
                player = Player.objects.create(user=request.user, room=room)
                room.player_count += 1
                room.save()

                return JsonResponse({'success': True})

            else:
                return render(request, 'GameRoom/join_room.html', {'rooms': rooms, 'error': 'The room is already full'})

        except GameRoom.DoesNotExist:
            return render(request, 'GameRoom/join_room.html', {'rooms': rooms, 'error': 'Room does not exist'})

    return render(request, 'GameRoom/join_room.html', {'rooms': rooms})


from django.shortcuts import redirect


@login_required(login_url='login')
def remove_player(request, room_code, player_id):
    try:
        room = GameRoom.objects.get(code=room_code)
        player = Player.objects.get(id=player_id, room=room)
    except GameRoom.DoesNotExist or Player.DoesNotExist:
        return redirect('GameRoom:room', room_code=room_code)

    if request.user == room.created_by:  # Pārbaudām, vai lietotājs ir istabas īpašnieks
        # Saglabājam izmetā lietotāja informāciju sesijā, lai to attēlotu menu lapā
        request.session['removed_player_username'] = player.user.username
        request.session['removed_player_email'] = player.user.email

        player.delete()  # Izmest lietotāju no istabas

        # Pārvietot izmeto spēlētāju uz menu lapu
        return redirect('menu')  # Aizstājiet 'menu' ar jūsu reālo URL uz menu lapu

    return redirect('GameRoom:room', room_code=room_code)



@login_required(login_url='login')
def change_owner(request, room_code, player_id):
    print("Pieprasījuma lietotājs:", request.user)

    # Iegūst `request.user` id
    request_user_id = request.user.id
    print(request_user_id)

    owner_player = get_object_or_404(Player, user_id=request_user_id, room__code=room_code)

    # Pārbauda, vai pašreizējais lietotājs ir istabas īpašnieks (owners)
    current_player = get_object_or_404(Player, id=player_id, room__code=room_code)
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


def fetch_players(request, room_code):
    room = GameRoom.objects.get(code=room_code)
    players = room.player_set.all()

    data = []
    for player in players:
        data.append({
            'username': player.user.username,
            'is_owner': player.is_owner,
        })

    return JsonResponse({'players': data})


from django.core import serializers

def get_rooms_api(request):
    rooms = GameRoom.objects.all() # Vajadzētu iegūt istabu datus pēc vajadzības
    room_data = [{'code': room.code} for room in rooms]
    return JsonResponse(room_data, safe=False)

from django.http import JsonResponse

@csrf_exempt
def check_user_status(request):
    if request.method == 'POST':
        # Šeit iegūstiet lietotāja statusu vai veiciet nepieciešamās darbības
        response_data = {'message': 'User status checked successfully'}
        return JsonResponse(response_data)
        room.player_count += 1
        room.save()
    else:
        # Ja pieprasījums nav POST metode, atgriez atbilstošu kļūdas atbildi
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)
    
@login_required(login_url='login')
def get_room_data(request):
    rooms = GameRoom.objects.all()
    room_data = [
        {
            'code': room.code,
            'player_count': room.player_count,
            'max_players': room.max_players,
            'is_private': room.is_private
        }
        for room in rooms
    ]
    return JsonResponse({'room_data': room_data})