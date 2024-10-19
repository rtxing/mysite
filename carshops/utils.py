import googlemaps
from django.conf import settings

def calculate_distance(lat1, lng1, lat2, lng2):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    origins = f"{lat1},{lng1}"
    destinations = f"{lat2},{lng2}"
    
    result = gmaps.distance_matrix(origins, destinations, mode="driving")

    try:
        distance_meters = result['rows'][0]['elements'][0]['distance']['value']
        distance_km = distance_meters / 1000
        return distance_km
    except (KeyError, IndexError):
        return None
