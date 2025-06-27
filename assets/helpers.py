import json

def load_airports_data(filepath='airports.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        airports = json.load(f)
    airports_dict = {airport['iata_code']: airport for airport in airports}
    return airports_dict