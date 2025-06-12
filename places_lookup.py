import googlemaps
import pprint
import time
import pandas as pd

# Define the API Key.
API_KEY = '****Your API KEY HERE****'

# Define the Client
gmaps = googlemaps.Client(key=API_KEY)



#get coordinates of current location and return lat/lon 
def get_coordinates_from_address(api_key, address):
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude
    else:
        print("Address not found.")
        return None, None




stored_results = []
# Do a simple nearby search where we specify the location
# in lat/lon format, along with a radius measured in meters
def extract_places():
    for place in places_result['results']:
        time.sleep(1)
        # define the place id, needed to get place details. Formatted as a string.
        my_place_id = place['place_id']

        #fields you would liked to return. Formatted as a list.
        my_fields = ['name', 'formatted_phone_number', 'formatted_address', 'geometry/location', 'type', 'rating','price_level']

        # make a request for the details.
        places_details = gmaps.place(place_id=my_place_id, fields=my_fields)
        pprint.pprint(places_details)
        name = places_details['result']['name']
        formatted_address = places_details['result']['formatted_address']
        latlng = places_details['result']['geometry']['location']
        place_type = places_details['result']['types']
        rating_score = places_details['result]['rating']
        price_level = places_details['result']['price_level]
        
        #get distance to location using origin coordinates and location coordinates
        origin_lat = coord.split(' ')[0]
        origin_long = coord.split(' ')[1]
        place_lat, place_long = latlng['lat'], latlng['lng']
        distance = gmaps.distance_matrix([origin_lat + " " + origin_long], [place_lat + " " + place_long], mode='driving')['rows'][0]['elements'][0]
        
        placeList = [name, formatted_address, latlng['lat'], latlng['lng'], place_type, rating_score, price_level, distance]
        stored_results.append(placeList)
    return stored_results


address = input("Enter your address: ")

lattitude, longitude = get_coordinates_from_address(API_KEY, address)

coord = "{0},{1}".format(lattitude, longitude)
rad = int(input("Enter radius of surrounding[in mts]:"))
typ = input("Enter type of place:")

params = {
    'location': coord,
    'radius': rad,
    'open_now': False,
    'type': typ
}

#Loop for next page
places_result = gmaps.places_nearby(**params)
if 'next_page_token' in places_result:
    while 'next_page_token' in places_result:
        places_result = gmaps.places_nearby(**params)
        new_stored_results = extract_places()
        if 'next_page_token' in places_result:
            params['page_token'] = places_result['next_page_token']
        else:
            break
else:
    places_result = gmaps.places_nearby(**params)
    new_stored_results = extract_places()

# -------------- Add Dataframe to EXCEL -----------------------
print("Addinig Values in Excel...")
# define the headers, that is just the key of each result dictionary.
# row_headers = stored_results[0].keys()
# create a new workbook and a new worksheet.
#create dataframe with specified columns
a = pd.DataFrame(new_stored_results, columns=['Name', 'Address', 'Latitude', 'Longitude', 'Type', 'Rating', 'Price Level', 'Disstance'])
#write dataframe out to excel
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
a.to_excel(writer, sheet_name='Place Details', index=False)
writer.close()
