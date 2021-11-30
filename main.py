import requests
import sys
from datetime import datetime
from os.path import exists, abspath, dirname, join
import json

class WeatherForecast:

    BASE_URL = 'http://api.weatherapi.com/v1/history.json'

    def __init__(self, api_key):
        self.api_key = api_key
        self.database_path = join(dirname(abspath(__file__)), 'database.txt')
        #sprawdzam czy istnieje plik database - jeśli tak to otwieram i zczytuję do database, jesli nie tworze pusta database
        if exists(self.database_path):
            with open(self.database_path, 'r') as file:
                self.database = json.loads(file.read())
        else:
            self.database = {}

    def get_data(self, date=str(datetime.today().date())):
        r = requests.get(f'{self.BASE_URL}?key={self.api_key}&q=Cracow&dt={date}')
        self.data = r.json()

    def get_rain_info(self):
        if 'forecast' in self.data:
            precip = float(self.data['forecast']['forecastday'][0]['day']['totalprecip_mm'])
            return self.get_rain_chance(precip)
        return 'Nie wiem!'

    def get_rain_chance(self, precip):
        if precip > 0.0:
            return "Bedzie padac"
        elif precip == 0.0:
            return "Nie bedzie padac"
        return "Nie wiem"

    def __getitem__(self, date=str(datetime.today().date())):
        if date in self.database:
            return self.database[date]
        self.get_data(date)
        new_info = self.get_rain_info()

        self.database[date] = new_info

        with open(self.database_path, 'w') as file:
            file.write(json.dumps(self.database))
        return new_info

    def items(self):
        for date, value in self.database.items():
            yield (date, value)


wf = WeatherForecast(api_key=sys.argv[1])
print(wf[sys.argv[2]])

print(list(wf.items()))
