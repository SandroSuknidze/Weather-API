import requests
import json
import sqlite3


response = requests.get(
  'https://api.stormglass.io/v2/weather/point',
  params={
    'lat': 58.7984,
    'lng': 17.8081,
    'params': 'waveHeight'

  },
  headers={
    'Authorization': '22e38440-b655-11eb-9cd1-0242ac130002-22e384f4-b655-11eb-9cd1-0242ac130002'
  }
)


json_data = response.json()
res = response.json()
print(res)
with open('weather.json', 'w') as f:
  json.dump(res, f, indent=4)

print(response.status_code)
print(response.headers)

for num in range (0,len(res["hours"])):
  print(res["hours"][num])



all = []
for i in res['hours']:
    time = i['time']
    meteo = i['waveHeight']['meteo']
    noaa = i['waveHeight']['noaa']
    sg = i['waveHeight']['sg']
    row = (time, meteo, noaa, sg)
    all.append(row)


conn = sqlite3.connect('weather.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS weather
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            time VARCHAR(20),
            meteo FLOAT,
            noaa FLOAT,
            sg FLOAT
            )''')

#შევქმენი ცხრილი ზემოთ მოცემული დასახელებებით
c.executemany('INSERT INTO weather (time, meteo, noaa, sg) VALUES (?, ?, ?, ?)', all)
#და ჩავსვი weather.json დან წამოღებული ინფორმაცია

conn.commit()
conn.close()