from skyplot_system_function import read_tle_file , skyplot
from tle_data_for_skyplot   import fetch_confirmation
import datetime

file_path = 'F:\\Project_RAIM\\Pre-Project\\data\\TLE2.txt'
TLE_Data = read_tle_file(file_path)
Sat_latitude = 13.75
Sat_longitude = 100.50
user_datetime = datetime.datetime(2025, 2, 23, 10, 0, 0)
Position = skyplot(Sat_latitude, Sat_longitude, TLE_Data, user_datetime)

#print(TLE_Data)