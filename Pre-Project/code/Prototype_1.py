import Library_GNSS as GNSS
import math
import csv


# Constants
EARTH_RADIUS = 6371e3  # Earth radius in meters
MIN_ELEVATION_ANGLE = 5  # Minimum elevation angle in degrees
MAX_DISTANCE = 5000e3  # Maximum radius in meters (5000 km)

# Convert degrees to radians
def deg_to_rad(deg):
    return deg * math.pi / 180

# Convert radians to degrees
def rad_to_deg(rad):
    return rad * 180 / math.pi

# Convert geodetic coordinates (lat, lon, alt) to ECEF coordinates
def geodetic_to_ecef(lat, lon, alt):
    lat_rad = deg_to_rad(lat)
    lon_rad = deg_to_rad(lon)
    R = EARTH_RADIUS + alt
    x = R * math.cos(lat_rad) * math.cos(lon_rad)
    y = R * math.cos(lat_rad) * math.sin(lon_rad)
    z = R * math.sin(lat_rad)
    return x, y, z

# Calculate the elevation angle of a satellite relative to the receiver
def calculate_elevation(receiver_pos, satellite_pos):
    rx, ry, rz = receiver_pos
    sx, sy, sz = satellite_pos
    
    # Vector from receiver to satellite
    dx = sx - rx
    dy = sy - ry
    dz = sz - rz
    
    # Distance from receiver to satellite
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    
    # Unit vector for the receiver position
    r_mag = math.sqrt(rx**2 + ry**2 + rz**2)
    rx_unit, ry_unit, rz_unit = rx / r_mag, ry / r_mag, rz / r_mag
    
    # Unit vector from receiver to satellite
    dx_unit, dy_unit, dz_unit = dx / dist, dy / dist, dz / dist
    
    # Dot product between the two unit vectors
    dot_product = rx_unit * dx_unit + ry_unit * dy_unit + rz_unit * dz_unit
    
    # Elevation angle: arcsin of the dot product
    elevation_angle = rad_to_deg(math.asin(dot_product))
    return elevation_angle

# Main function
def find_visible_and_close_satellites(receiver_lat, receiver_lon, receiver_alt, satellite_file, output_file):
    receiver_pos = geodetic_to_ecef(receiver_lat, receiver_lon, receiver_alt)
    visible_satellites = []
    close_satellites = []

    with open(satellite_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            sat_id, sat_lat, sat_lon, sat_alt = row[0], float(row[1]), float(row[2]), float(row[3])
            satellite_pos = geodetic_to_ecef(sat_lat, sat_lon, sat_alt)
            
            # Calculate distance and elevation angle
            distance = calculate_distance(receiver_pos, satellite_pos)
            elevation_angle = calculate_elevation(receiver_pos, satellite_pos)
            
            # Debugging outputs
            print(f"Satellite {sat_id}: Distance = {distance} meters, Elevation = {elevation_angle}°")
            
            if distance <= MAX_DISTANCE:
                close_satellites.append((sat_id, distance))
            
            if elevation_angle > MIN_ELEVATION_ANGLE:
                visible_satellites.append((sat_id, elevation_angle))
    
    # Save results to output CSV
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Satellite ID', 'Elevation Angle (degrees)', 'Distance (meters)'])
        for sat in visible_satellites:
            sat_id = sat[0]
            distance = next((c[1] for c in close_satellites if c[0] == sat_id), None)
            writer.writerow([sat_id, sat[1], distance])

    print(f"Results saved to {output_file}")

# Helper: Calculate the distance between two ECEF points
def calculate_distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return math.sqrt(dx**2 + dy**2 + dz**2)


# File path to save the TLE data
file_path = 'F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt'

#GNSS.fetch_tle_data_txt(file_path)

#print("TLE data fetched and saved to file.")

sat_obj = GNSS.read_tle_file(file_path)

print("TLE data read from file.")

output_filename = 'F:\\Project_RAIM\\Pre-Project\\data\\POS.csv'
# Date and time for which the position is to be computed (UTC + 7)
year = 2024
month = 11
day = 19
hour = 16
minute = 15
second = 0

# Convert UTC+7 to UTC
hour_utc = hour - 7
if hour_utc < 0:
    hour_utc += 24
    day -= 1


# Demo Receiver Position
receiver_lat = 13.683529
receiver_lon = 100.619786
receiver_alt = 20000


position_data = GNSS.compute_positions(sat_obj, year, month, day, hour_utc, minute, second)

GNSS.save_positions_to_file(position_data, output_filename, year, month, day, hour_utc, minute, second)

satellite_file = "F:\\Project_RAIM\\Pre-Project\\data\\POS.csv"
output_file = "F:\\Project_RAIM\\Pre-Project\\data\\VISIBLE.csv"

find_visible_and_close_satellites(receiver_lat, receiver_lon, receiver_alt, satellite_file, output_file)

