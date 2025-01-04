from skyplot_system_function import read_tle_file , skyplot
from tle_data_for_skyplot   import fetch_confirmation

file_path = "C:\\RAIM Test\\TLE_Data\\TLE_Data.txt"
TLE_Data = read_tle_file(file_path)
Sat_latitude = 13.44
Sat_longitude = 100.30
Position = skyplot(Sat_latitude, Sat_longitude, TLE_Data)

#print(TLE_Data)