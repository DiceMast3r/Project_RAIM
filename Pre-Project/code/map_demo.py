import folium
import csv


# read the data from the csv file

# File path to the CSV file
file_path = "F:\\Project_RAIM\\Pre-Project\\data\\extracted_waypoints.csv"

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
map = folium.Map(location=map_center, zoom_start=map_zoom)

# Add markers for each waypoint
for name, latitude, longitude in waypoints:
    folium.Marker(location=[latitude, longitude], popup=name).add_to(map)


# draw lines between the waypoints
for i in range(len(waypoints) - 1):
    start = waypoints[i][1], waypoints[i][2]
    end = waypoints[i + 1][1], waypoints[i + 1][2]
    folium.PolyLine(locations=[start, end], color='red').add_to(map)


map.show_in_browser()
