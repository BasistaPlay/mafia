import schedule
import time
from .models import GameRoom
from django.utils import timezone


def check_and_delete_empty_rooms():
    empty_rooms = GameRoom.objects.filter(player_count=0)

    for room in empty_rooms:
        # Iegūstam laiku, kad istaba tika pēdējo reizi atjaunināta
        # Iepriekš definējiet atbilstoši jūsu modeļa laukam
        last_updated = room.last_updated
        current_time = timezone.now()  # Importējiet timezone no django.utils

        # Aprēķinam laika starpību
        time_difference = current_time - last_updated

        # Ja istaba ir bijusi tukša 15 sekundes vai ilgāk, tad to dzēšam
        if time_difference.total_seconds() >= 1:
            room.delete()

# Šī funkcija uzstāda regulāru darbību


def schedule_empty_rooms_check():
    # Iestatiet izpildes biežumu (šajā piemērā ik pēc 15 sekundēm)
    schedule.every(15).seconds.do(check_and_delete_empty_rooms)

# Palaidiet funkciju, kas uzstāda regulāro darbību


def start_schedule():
    schedule_empty_rooms_check()

# Šī funkcija ļauj palaidīt plānotās darbības


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Izsaukiet šo funkciju, lai palaidītu plānotās darbības
if __name__ == "__main__":
    start_schedule()
    run_scheduled_tasks()
