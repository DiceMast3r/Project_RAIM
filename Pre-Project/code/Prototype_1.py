import Library_GNSS as GNSS

# File path to save the TLE data
file_path = 'F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt'

GNSS.fetch_tle_data_txt(file_path)

print("TLE data fetched and saved to file.")

sat_obj = GNSS.read_tle_file(file_path)

print("TLE data read from file.")

output_filename = 'F:\\Project_RAIM\\Pre-Project\\data\\POS.csv'
# Date and time for which the position is to be computed (UTC + 7)
year = 2024
month = 11
day = 6
hour = 0
minute = 5
second = 0

# Convert UTC+7 to UTC
hour_utc = hour - 7
if hour_utc < 0:
    hour_utc += 24
    day -= 1



position_data = GNSS.compute_positions(sat_obj, year, month, day, hour_utc, minute, second)

GNSS.save_positions_to_file(position_data, output_filename, year, month, day, hour_utc, minute, second)

