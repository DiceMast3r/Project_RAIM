import folium
import csv
import math


# Function to calculate the distance between two points given their coordinates

def calculate_distance(start, end):
    # Constants for Earth radius and conversion factor from meters to kilometers
    EARTH_RADIUS = 6371000  # in meters
    METERS_TO_KM = 1 / 1000

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = start
    lat2, lon2 = end
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate the change in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the distance using the Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS * c

    return distance * METERS_TO_KM

# File path to the CSV file
file_path = "D:\\Project_RAIM\\Pre-Project\\data\\extracted_waypoints.csv"

# List to store the waypoints
waypoints = []

# Open the CSV file and read the data
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    for row in reader:
        name, latitude, longitude = row
        waypoints.append((name, float(latitude), float(longitude)))
        

# Create a map centered at the given latitude and longitude
map_center = [13.7563, 100.5018]
map_zoom = 5
map_title = "Map"

# Create a map object using the specified parameters
map_waypoint = folium.Map(location=map_center, zoom_start=map_zoom)

# Add markers for each waypoint
for name, latitude, longitude in waypoints:
    folium.Marker(location=[latitude, longitude], popup=name).add_to(map_waypoint)


# draw lines between the waypoints
for i in range(len(waypoints) - 1):
    start = waypoints[i][1], waypoints[i][2]
    end = waypoints[i + 1][1], waypoints[i + 1][2]
    folium.PolyLine(locations=[start, end], color='red').add_to(map_waypoint)

# calculate the distance between the waypoints and show when the user clicks on the marker
for i in range(len(waypoints) - 1):
    start = waypoints[i][1], waypoints[i][2]
    end = waypoints[i + 1][1], waypoints[i + 1][2]
    distance = calculate_distance(start, end)
    popup_content = f"{waypoints[i][0]}<br>Distance to next point: {distance:.2f} km"
    folium.Marker(location=start, popup=popup_content).add_to(map_waypoint)

map_waypoint.show_in_browser()
