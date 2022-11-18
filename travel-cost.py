import requests
from bs4 import BeautifulSoup

# API GOOGLE MAPS https://developers.google.com/maps/documentation/distance-matrix/get-api-key
api_key = ''  # Insert your API KEY
git add .
# INFO FROM USERS
origin = input('Podaj miejsce z którego wyruszasz: ')
destination = input('Podaj miejsce do którego jedziesz: ')
car_fuel = input('Podaj jakiego paliwa używasz (95, 98, ON, ON+, LPG) Wybierz jedno: ')
fuel_consuption = float(input('Podaj jakie masz średnie spalanie auta: '))

# URL for request

url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}'


# Get average fuel price from https://www.autocentrum.pl/paliwa/ceny-paliw/

def get_petrol_price():
    response = requests.get('https://www.autocentrum.pl/paliwa/ceny-paliw/')
    soup = BeautifulSoup(response.content, 'html.parser')
    fuels_pricing = {
        div.get_text(): div.findNextSibling('div').get_text().replace('\n', '').replace('zł', '').replace(' ', '')
        for div in soup.select('.fuel-header')}
    return fuels_pricing


# Get average fuels prices from function
fuels_pricing = get_petrol_price()

# Get distance from google maps API request
response = requests.get(url)
body = response.json()
distance = body['rows'][0]['elements'][0]['distance']

# Fuel price from string to float
fuel_price = float(fuels_pricing[car_fuel].replace(',', '.'))

if origin == '' or destination == '':
    print('Podaj prawidłowe wartości')
else:
    cost = fuel_price * distance['value'] / 1000 * fuel_consuption / 100
    print(f'Koszt spalania to: {round(cost, 2)} zł')
