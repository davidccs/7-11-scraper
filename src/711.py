import json
import requests
import sys

def pretty_print_json(json_text):
	json_text = json.dumps(json_text)
	parsed = json.loads(json_text)
	print(json.dumps(parsed, indent=4))
	
	return None


def fuel_prices(jsonResponse, fuelType):
	
	stations = jsonResponse['stations']
	prices = jsonResponse['prices']

	dict_711 = {}
	
	for station in stations:
		if station['brand'] == '7-Eleven':
			key = station
			for price in prices:
				if station['code'] == price['stationcode'] and price['fueltype'] == fuelType:
						dict_711[station['address']] = price['price']
	
	return dict_711

def order_fuel_prices(parse_dict):
	dict_711 = {}
	for element in sorted (parse_dict, key=parse_dict.get):
			dict_711[element] = parse_dict[element]
	# pretty_print_json(dict_711)
	return dict_711

def print_cheapest_prices(parse_dict, fuelType, top):
		
	cheapest_prices = fuel_prices(parse_dict, fuelType)
	cheapest_prices = order_fuel_prices(cheapest_prices)
	
	print("-- Cheapest 7-11 Fuel for %s --" % fuelType)
	i = 0
	for key, value in cheapest_prices.items():
		if i == top:
			break
		print("Address: %s and Price: %s/L" % (key, value))
		i = i + 1

def auth():

	url = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"

	querystring = {"grant_type":"client_credentials"}

	headers = {
		'content-type': "application/json",
		'authorization': "MU1ZU1JBeDV5dnFIVVpjNlZHdHhpeDZvTUEycWdmUlQ6Qk12V2FjdzE1RXQ4dUZHRg=="
	}
	
	response = requests.request("GET", url, headers=headers, params=querystring)

	jsonResponse = response.json()

	accessToken = jsonResponse['access_token']

	url = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices"

	headers = {
		'content-type': "application/json",
		'authorization': "Bearer " + accessToken,
		'apikey': "1MYSRAx5yvqHUZc6VGtxix6oMA2qgfRT",
		'transactionid': "2",
		'requesttimestamp': "30/11/2020 10:50:10 AM"
	}

	response = requests.request("GET", url, headers=headers)
	jsonResponse = response.json()
	
	return jsonResponse


def main():
	jsonResponse = auth()
	try:
		print_cheapest_prices(jsonResponse, sys.argv[1], int(sys.argv[2]))
	except:
		print("Must include Type of Fuel and amount shown")
		print("Different Fuel Types E10, P95 and P98")
if __name__ == "__main__":
	main()


