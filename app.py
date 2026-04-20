import requests
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def get_weather_data():
    api_key ="bd059eda78fb1feb44e76d9c331ba2d1"
    city = "Fes"
    
    # رابط التوقعات (Forecast) كيعطينا كاع التفاصيل
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=en"
    
    response = requests.get(url)
    data = response.json()

    # 1. الجو الحالي
    current = {
        'city': data['city']['name'],
        'temp': round(data['list'][0]['main']['temp']),
        'desc': data['list'][0]['weather'][0]['description'],
        'icon': data['list'][0]['weather'][0]['icon'],
        'humidity': data['list'][0]['main']['humidity'],
        'wind': round(data['list'][0]['wind']['speed']),
        'date': datetime.now().strftime('%A %H:%M')
    }

    # 2. التوقعات ديال الساعات (أول 8 ساعات - للمنحنى)
    hourly = []
    for item in data['list'][:8]:
        hourly.append({
            'time': datetime.fromtimestamp(item['dt']).strftime('%H:00'),
            'temp': round(item['main']['temp'])
        })

    # 3. التوقعات ديال 5 أيام (يوم واحد من كل 24 ساعة)
    forecast_days = []
    for i in range(0, 40, 8): # كينقز بـ 8 حيت الـ API فيه توقع كل 3 ساعات
        day_data = data['list'][i]
        forecast_days.append({
            'day': datetime.fromtimestamp(day_data['dt']).strftime('%a'),
            'temp': round(day_data['main']['temp']),
            'icon': day_data['weather'][0]['icon']
        })

    return current, hourly, forecast_days

@app.route('/')
def home():
    try:
        current, hourly, forecast = get_weather_data()
        return render_template('index.html', weather=current, hourly=hourly, forecast=forecast)
    except:
        return "Check your API Key or Internet Connection!"

if __name__ == '__main__':
    app.run(debug=True)