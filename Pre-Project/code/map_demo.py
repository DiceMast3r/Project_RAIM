import folium
import csv
import math
from datetime import datetime, timedelta
import data_handler as dh

# Function to calculate the distance between two points given their coordinates
def calculate_distance(start, end):
    # Constants for Earth radius and conversion factor from meters to kilometers
    EARTH_RADIUS = 6371000  # in meters
    METERS_TO_KM = 1 / 1000

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [start[0], start[1], end[0], end[1]])

    # Calculate the change in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the distance using the Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS * c

    return distance * METERS_TO_KM

# Function to predict the arrival time at each waypoint
def predict_arrival_times(waypoints, speed_kmh, start_time):
    arrival_times = [start_time]
    for i in range(len(waypoints) - 1):
        start = waypoints[i][1], waypoints[i][2]
        end = waypoints[i + 1][1], waypoints[i + 1][2]
        distance = calculate_distance(start, end)
        travel_time = distance / speed_kmh  # in hours
        arrival_time = arrival_times[-1] + timedelta(hours=travel_time)
        arrival_times.append(arrival_time)
    return arrival_times

# Function to read waypoints from a CSV file
def read_waypoints(file_path):
    waypoints = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, latitude, longitude = row
            waypoints.append((name, float(latitude), float(longitude)))
    return waypoints

# Function to create a map with waypoints and lines between them
def create_map(waypoints, map_center, map_zoom):
    map_waypoint = folium.Map(location=map_center, zoom_start=map_zoom)
    for name, latitude, longitude in waypoints:
        folium.Marker(location=[latitude, longitude], popup=name).add_to(map_waypoint)
    for i in range(len(waypoints) - 1):
        start = waypoints[i][1], waypoints[i][2]
        end = waypoints[i + 1][1], waypoints[i + 1][2]
        folium.PolyLine(locations=[start, end], color='red').add_to(map_waypoint)
    return map_waypoint

# Function to add arrival time and satellite data to map markers
def add_marker_data(map_waypoint, waypoints, arrival_times):
    for i in range(len(waypoints) - 1):
        start = waypoints[i][1], waypoints[i][2]
        distance = calculate_distance(start, waypoints[i + 1][1:3])
        arrival_time = arrival_times[i].strftime("%Y-%m-%d %H:%M:%S")
        year, month, day, hour, minute, second = arrival_times[i].timetuple()[:6]
        pdop, sat_view, sat_tot = dh.compute_satellite_data(year, month, day, hour, minute, second, start[0], start[1], 0)
        popup_content = f"{waypoints[i][0]}<br>Distance to next point: {distance:.2f} km<br>Arrival time: {arrival_time}<br>Predicted PDOP: {pdop:.5f}<br>Number of satellites in view: {sat_view}<br>Total number of satellites: {sat_tot}"
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(location=start, popup=popup).add_to(map_waypoint)
    # Handle the last waypoint separately
    last_waypoint = waypoints[-1]
    arrival_time = arrival_times[-1].strftime("%Y-%m-%d %H:%M:%S")
    year, month, day, hour, minute, second = arrival_times[-1].timetuple()[:6]
    pdop, sat_view, sat_tot = dh.compute_satellite_data(year, month, day, hour, minute, second, last_waypoint[1], last_waypoint[2], 0)
    popup_content = f"{last_waypoint[0]}<br>Arrival time: {arrival_time}<br>Predicted PDOP: {pdop:.5f}<br>Number of satellites in view: {sat_view}<br>Total number of satellites: {sat_tot}"
    popup = folium.Popup(popup_content, max_width=300)
    folium.Marker(location=(last_waypoint[1], last_waypoint[2]), popup=popup).add_to(map_waypoint)

def main():
    # File path to the CSV file
    file_path = "F:\\Project_RAIM\\Pre-Project\\data\\extracted_waypoints.csv"
    waypoints = read_waypoints(file_path)
    
    # Create a map centered at the given latitude and longitude
    map_center = [13.7563, 100.5018]
    map_zoom = 5
    map_waypoint = create_map(waypoints, map_center, map_zoom)
    
    # Predict arrival times
    speed_kmh = 800.0  # Example speed in km/h
    start_time = datetime.now()
    arrival_times = predict_arrival_times(waypoints, speed_kmh, start_time)
    
    # Add marker data
    add_marker_data(map_waypoint, waypoints, arrival_times)
    
    map_waypoint.show_in_browser()

if __name__ == "__main__":
    main()