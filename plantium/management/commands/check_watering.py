from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date
from plantium.models import Crop  

class Command(BaseCommand):
    help = 'Envía recordatorios de riego para cultivos con frecuencia de 2 días'

    def handle(self, *args, **options):
        today = date.today()
        users_alerts = {}

        crops = list(Crop.objects.exclude(last_watering__isnull=True))
        
        for crop in crops:
            if not crop.last_watering:
                continue

            days_since_watering = (today - crop.last_watering).days
            freq = crop.plant.watering_freq

            if days_since_watering == freq - 1:
                alert_type = 'tomorrow'
            elif days_since_watering == freq:
                alert_type = 'today'
            else:
                continue

            if crop.user not in users_alerts:
                users_alerts[crop.user] = {'today': [], 'tomorrow': []}
            users_alerts[crop.user][alert_type].append(crop)

        for user, crops in users_alerts.items():
            if crops['today'] or crops['tomorrow']:
                self.send_alert(user, crops)

        self.stdout.write(self.style.SUCCESS(f'Se procesaron {len(users_alerts)} usuarios con alertas.'))

    def send_alert(self, user, crops):
        subject = '🌱 Recordatorio de riego de Plantium'

        html_message = render_to_string('emails/watering_alert.html', {
            'user': user,
            'crops_today': crops['today'],
            'crops_tomorrow': crops['tomorrow'],
        })
        
        plain_message = f"Hola {user.username},\n\n"
        if crops['today']:
            plain_message += "HOY debes regar:\n"
            for crop in crops['today']:
                plain_message += f"- {crop.name} ({crop.plant.name})\n"
        if crops['tomorrow']:
            plain_message += "\nMAÑANA debes regar:\n"
            for crop in crops['tomorrow']:
                plain_message += f"- {crop.name} ({crop.plant.name})\n"

        # envia el correo
        send_mail(
            subject,
            plain_message,
            None,  # default (plantiumproject@gmail.com)
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
