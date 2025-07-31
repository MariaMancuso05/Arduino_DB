from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import LightEvent, LightStatus
import json

@csrf_exempt
def receive_light_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Estrai stato dal messaggio
            stato = data.get('stato')  # 'acceso' o 'spento'
            
            # Crea nuovo evento
            evento = LightEvent.objects.create(
                stato=stato,
            )
            
            # Aggiorna stato corrente (opzionale)
            status, created = LightStatus.objects.get_or_create(id=1)
            status.is_on = (stato == 'acceso')
            status.save()
            
            return JsonResponse({
                'status': 'ok',
                'message': f'Luce {stato} registrata',
                'timestamp': evento.timestamp.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON non valido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Solo POST permesso'}, status=405)

def get_current_status(request):
    """Vista opzionale per controllare lo stato corrente"""
    try:
        status = LightStatus.objects.get(id=1)
        ultimo_evento = LightEvent.objects.first()
        
        return JsonResponse({
            'luce_accesa': status.is_on,
            'ultimo_cambio': status.ultimo_cambio.isoformat(),
            'ultimo_evento': {
                'stato': ultimo_evento.stato if ultimo_evento else None,
                'timestamp': ultimo_evento.timestamp.isoformat() if ultimo_evento else None
            }
        })
    except LightStatus.DoesNotExist:
        return JsonResponse({'luce_accesa': None, 'message': 'Nessuno stato registrato'})

def dashboard(request):
    """Vista per visualizzare gli eventi"""
    eventi = LightEvent.objects.all()[:50]  # Ultimi 50 eventi
    stato_corrente = LightStatus.objects.first()
    
    # Calcola statistiche
    totale_accensioni = LightEvent.objects.filter(stato='acceso').count()
    totale_spegnimenti = LightEvent.objects.filter(stato='spento').count()
    
    context = {
        'eventi': eventi,
        'stato_corrente': stato_corrente,
        'totale_accensioni': totale_accensioni,
        'totale_spegnimenti': totale_spegnimenti,
    }
    return render(request, 'api/light_dashboard.html', context)

def dashboard_data(request):
    """API endpoint per dati dashboard in JSON"""
    eventi = LightEvent.objects.all()[:20]
    stato_corrente = LightStatus.objects.first()
    
    # IMPORTANTE: Usa timezone.localtime() per convertire da UTC a Europe/Rome
    eventi_data = [{
        'stato': e.get_stato_display(),
        'timestamp': timezone.localtime(e.timestamp).strftime('%d/%m/%Y %H:%M:%S'),
    } for e in eventi]
    
    return JsonResponse({
        'is_on': stato_corrente.is_on if stato_corrente else False,
        'ultimo_cambio': timezone.localtime(stato_corrente.ultimo_cambio).strftime('%d/%m/%Y %H:%M:%S') if stato_corrente else None,
        'totale_accensioni': LightEvent.objects.filter(stato='acceso').count(),
        'totale_spegnimenti': LightEvent.objects.filter(stato='spento').count(),
        'eventi': eventi_data
    })