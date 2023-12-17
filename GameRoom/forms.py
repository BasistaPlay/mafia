from django import forms
from .models import GameRoom

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = GameRoom
        fields = ['code', 'max_players', 'is_private', 'password']  # Pievieno password lauku

class JoinRoomForm(forms.Form):
    room_code = forms.CharField(label='Room Code', max_length=10)
    password = forms.CharField(label='Password', max_length=50, required=False)  # Password tagad ir nepieciešams ievadīt
