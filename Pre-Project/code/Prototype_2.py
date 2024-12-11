import math
import csv
import Library_GNSS as GNSS


# Constants
EARTH_RADIUS = 6371e3  # Earth radius in meters

# Convert degrees to radians
def deg_to_rad(deg):
    return deg * math.pi / 180

# Convert geodetic coordinates (lat, lon, alt) to ECEF coordinates
def geodetic_to_ecef(lat, lon, alt):
    lat_rad = deg_to_rad(lat)
    lon_rad = deg_to_rad(lon)
    R = EARTH_RADIUS + alt
    x = R * math.cos(lat_rad) * math.cos(lon_rad)
    y = R * math.cos(lat_rad) * math.sin(lon_rad)
    z = R * math.sin(lat_rad)
    return x, y, z

# Calculate the distance between two ECEF points
def calculate_distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return math.sqrt(dx**2 + dy**2 + dz**2)

# Main function
def calculate_and_save_distances(receiver_lat, receiver_lon, receiver_alt, satellite_file, output_file):
    receiver_pos = geodetic_to_ecef(receiver_lat, receiver_lon, receiver_alt)

    # Open the input satellite file and output distance file
    with open(satellite_file, 'r') as csvfile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(outfile)

        # Write header to the output file
        writer.writerow(['Satellite ID', 'Distance (km)'])

        # Skip the header of the input file
        next(reader)

        for row in reader:
            sat_id, sat_lat, sat_lon, sat_alt = row[0], float(row[1]), float(row[2]), float(row[3])
            satellite_pos = geodetic_to_ecef(sat_lat, sat_lon, sat_alt)

            # Calculate distance
            distance = calculate_distance(receiver_pos, satellite_pos)
            distance = distance / 1000  # Convert to kilometers
            distance = round(distance, 6)  # Round to 2 decimal places

            # Debugging output
            print(f"Satellite {sat_id}: Distance = {distance} km")

            # Write the result to the output file
            writer.writerow([sat_id, distance])

    print(f"Distances saved to {output_file}")
    

# filter a sattelite based on the distance

def filter_satellites(satellite_file, output_file, distance_threshold):
    with open(satellite_file, 'r') as csvfile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(outfile)

        # Write header to the output file
        writer.writerow(['Satellite ID', 'Distance (km)'])

        # Skip the header of the input file
        next(reader)

        for row in reader:
            sat_id, sat_distance = row[0], float(row[1])
            if sat_distance <= distance_threshold:
                writer.writerow([sat_id, sat_distance])
            else:
                print(f"Satellite {sat_id} is too far away ({sat_distance} km), skipping")
                
    print(f"Filtered satellites saved to {output_file}")



debug_machine = 2 # 1 = PC, 2 = Laptop

if debug_machine == 1:
    file_path = 'F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt' # File path to save the TLE data
    output_filename = 'F:\\Project_RAIM\\Pre-Project\\data\\POS.csv' # File path to save the position data
    output_filename_ecef = 'F:\\Project_RAIM\\Pre-Project\\data\\POS_ECEF.csv'
elif debug_machine == 2:
    file_path = 'D:\\Project_RAIM\\Pre-Project\\data\\TLE.txt' # File path to save the TLE data
    output_filename = 'D:\\Project_RAIM\\Pre-Project\\data\\POS.csv' # File path to save the position data
    output_filename_ecef = 'D:\\Project_RAIM\\Pre-Project\\data\\POS_ECEF.csv'
else:
    print("Invalid debug machine setting.")
    exit()


#GNSS.fetch_tle_data_txt(file_path)

#print("TLE data fetched and saved to file.")

sat_obj = GNSS.read_tle_file(file_path)

print("TLE data read from file.")

# Date and time for which the position is to be computed (UTC + 7)
year = 2024
month = 12
day = 7
hour = 17
minute = 55
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
output_file = "F:\\Project_RAIM\\Pre-Project\\data\\DISTANCE.csv"
filter_output_file = "F:\\Project_RAIM\\Pre-Project\\data\\CLOSE.csv"

calculate_and_save_distances(receiver_lat, receiver_lon, receiver_alt, satellite_file, output_file)
filter_satellites(output_file, filter_output_file, 3000)