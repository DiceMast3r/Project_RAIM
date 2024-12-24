import Library_GNSS as GNSS

tle_file_path = "F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt"

def init_sat_obj(tle_file_path):
    sat_obj = GNSS.read_tle_file(tle_file_path)
    print("TLE data read from file.")
    return sat_obj

def compute_ecef_positions(year, month, day, hour, minute, second):
    ini_sat_obj = init_sat_obj(tle_file_path)
    position_data_ecef = GNSS.compute_positions_ecef(ini_sat_obj, year, month, day, hour, minute, second)
    return position_data_ecef

def compute_neu_positions(ecef_list, origin_lat, origin_lon):
    position_NEU = GNSS.compute_positions_neu_direct(ecef_list, origin_lat, origin_lon)
    return position_NEU

def compute_azel_positions(neu_list):
    az_el = GNSS.compute_positions_azel_direct(neu_list)
    return az_el

# Date and time for which the position is to be computed (UTC + 7)
year = 2024
month = 12
day = 12
hour = 19
minute = 20
second = 0

# Convert UTC+7 to UTC
hour_utc = hour - 7
if hour_utc < 0:
    hour_utc += 24
    day -= 1


origin_lat = 13.683529
origin_lon = 100.619786


ecef_list = compute_ecef_positions(year, month, day, hour_utc, minute, second)
neu_list = compute_neu_positions(ecef_list, origin_lat, origin_lon)
az_el_list = compute_azel_positions(neu_list)
