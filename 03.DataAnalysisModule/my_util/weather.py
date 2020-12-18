import requests

def get_weather(lat=37.550966, lng=126.849532):
    key_fd = open('./my_util/openweatherkey.txt', mode='r')
    oweather_key = key_fd.read(100)
    key_fd.close()

    open_weather = 'http://api.openweathermap.org/data/2.5/weather'
    url = f'{open_weather}?lat={lat}&lon={lng}&appid={oweather_key}&units=metric&lang=kr'
    result = requests.get(url).json()

    desc = result['weather'][0]['description']
    icon_code = result['weather'][0]['icon']
    icon_url = f'http://openweathermap.org/img/w/{icon_code}.png'
    temp = result['main']['temp']
    temp_min = result['main']['temp_min']
    temp_max = result['main']['temp_max']
    temp = round(float(temp)+0.01, 1)

    html = f'''<img src="{icon_url}" height="32"><strong>{desc}</strong>, 
                온도: <strong>{temp}&#8451</strong>, {temp_min}/{temp_max}&#8451'''
    return html