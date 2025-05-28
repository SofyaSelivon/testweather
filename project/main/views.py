from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import requests

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')


def meteo(request):
    city = request.GET.get('city', 'Moscow')

    try:
        meteo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        meteo_resp = requests.get(meteo_url).json()

        if not meteo_resp.get('results'):
            return render(request, 'index.html', {'error': 'Этого города нет в списке, попробуйте другой'})

        lat = meteo_resp['results'][0]['latitude']
        lon = meteo_resp['results'][0]['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url).json()

        return render(request, 'index.html', {
            'Город': city,
            'Температура': weather_resp['current_weather']['temperature'],
        })

    except Exception as e:
        return render(request, 'index.html', {'error': f'Произошла ошибка: {str(e)}'})