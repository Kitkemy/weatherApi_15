import requests
import sys
import pprint
from datetime import datetime

class WeatherForecast:

    BASE_URL = 'http://api.weatherapi.com/v1/history.json'

    def __getitem__(self, date):
        print('getItem')
        self.date = date

    def __init__(self, api_key, date=str(datetime.today().date())):
        self.api_key = api_key
        self.date = date
        self.data = self.get_data()

    def get_data(self):
            r = requests.get(f'{self.BASE_URL}?key={self.api_key}&q=Cracow&dt={self.date}')
            content = r.json()
            return content
    
    def get_rain_info(self):
        if 'error' in self.data:
            print(self.data['error']['message'])
            precip = -1
            return self.get_rain_chance(precip)
        else:
            precip = float(self.data['forecast']['forecastday'][0]['day']['totalprecip_in'])
            forecast = self.get_rain_chance(precip)
            #print(forecast)
            return forecast
    
    def get_rain_chance(self, precip):
        if precip > 0.0:
            return "Bedzie padac"
        elif precip == 0.0:
            return "Nie bedzie padac"
        else:
            return "Nie wiem"

if len(sys.argv) >= 3:
    date = sys.argv[2]
else:
    date = datetime.today().date()
      
weather = WeatherForecast(api_key = sys.argv[1],date=date)
#pprint.pprint(weather.get_data())


class Own_database:

    def __init__(self):
        self.database = []

    def open_file(self):
        pass

    def save_file(self):
        pass


database = []

try:
    file = open('database.txt', 'r')
    for line in file.readlines():
        splitted_line = line.split(';')
        database.append([splitted_line[0], splitted_line[1].replace('\n', '')])
    file.close()
except FileNotFoundError:
    pass

for date in database:
    if date[0] == weather.date:
        # no request
        print(date[1])
        sys.exit()

weather = WeatherForecast(api_key=sys.argv[1], date=sys.argv[2])
rain_info = weather.get_rain_info()
database.append([weather.date, rain_info])
print(rain_info)

with open('database.txt', 'w') as file:
    rows = ''
    for row in database:
        rows = rows + row[0] + ';' + row[1] + '\n'
    file.write(rows)

'''weather[2021-11-20]
rain_info = weather.get_rain_info()
database.append([weather.date, rain_info])
print(rain_info)
'''
