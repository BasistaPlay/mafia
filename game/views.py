from django.shortcuts import render, redirect
from django.http import JsonResponse
from GameRoom.models import Player, GameRoom
from django.urls import reverse


from django.http import JsonResponse

def start_game(request, room_code):
    if request.method == 'POST':
        player_ids = request.POST.getlist('player_ids[]')
        room = GameRoom.objects.get(code=room_code)
        player_count = Player.objects.filter(room__code=room_code).count()

        if player_count == room.max_players:
            if request.POST.get('csrfmiddlewaretoken') == request.COOKIES['csrftoken']:
                # Pieprasījums ar CSRF žetonu ir korekts
                # Veiciet vajadzīgās darbības, lai sāktu spēli
                game_url = reverse('game_page')  # Izmantojiet pareizo reverse ceļu
                return JsonResponse({'success': True, 'game_url': game_url})
            else:
                return JsonResponse({'success': False, 'error_message': 'Invalid CSRF token'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Not enough players'})
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def game_page(request):
    # Izmantojiet render funkciju, lai atgrieztu vajadzīgo skatu
    return render(request, 'game/game.html')