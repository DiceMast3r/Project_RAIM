import Library_GNSS as GNSS
import math


# Constants
EARTH_RADIUS = 6371e3  # Earth radius in meters

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



# File path to save the TLE data
file_path = 'F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt'

#GNSS.fetch_tle_data_txt(file_path)

#print("TLE data fetched and saved to file.")

sat_obj = GNSS.read_tle_file(file_path)

print("TLE data read from file.")

latlon_file = "F:\\Project_RAIM\\Pre-Project\\data\\POS.csv"
ecef_file = "F:\\Project_RAIM\\Pre-Project\\data\\POS_ECEF.csv"
neu_file = "F:\\Project_RAIM\\Pre-Project\\data\\POS_NEU.csv"
azel_file = "F:\\Project_RAIM\\Pre-Project\\data\\AZEL.csv"

# Date and time for which the position is to be computed (UTC + 7)
year = 2024
month = 12
day = 22
hour = 23
minute = 25
second = 5

# Convert UTC+7 to UTC
hour_utc = hour - 7
if hour_utc < 0:
    hour_utc += 24
    day -= 1

origin_lat = 13.75
origin_lon = 100.50
receiver_alt = 20


position_data_latlon = GNSS.compute_positions(sat_obj, year, month, day, hour_utc, minute, second)
GNSS.save_positions_to_file(position_data_latlon, latlon_file, year, month, day, hour_utc, minute, second)

position_data_ecef = GNSS.compute_positions_ecef(sat_obj, year, month, day, hour_utc, minute, second)

GNSS.save_position_to_file_ecef(position_data_ecef, ecef_file, year, month, day, hour_utc, minute, second)

position_NEU = GNSS.compute_positions_neu(ecef_file, origin_lat, origin_lon, receiver_alt)

GNSS.save_positions_to_file_neu(position_NEU, neu_file, origin_lat, origin_lon, receiver_alt)

az_el = GNSS.compute_positions_azel(neu_file)

GNSS.save_positions_to_file_azel(az_el, azel_file, origin_lat, origin_lon)


