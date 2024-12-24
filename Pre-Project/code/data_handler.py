import Library_GNSS as GNSS
import numpy as np

tle_file_path = "F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt"


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
origin_alt = 0


ecef_list = GNSS.compute_ecef_positions(
    tle_file_path, year, month, day, hour_utc, minute, second
)
pdop = (
    GNSS.cal_pdop(
        GNSS.extract_ecef_pos(ecef_list),
        GNSS.latlon_to_ecef(origin_lat, origin_lon, origin_alt),
    )
    / 1000
)
neu_list = GNSS.compute_neu_positions(ecef_list, origin_lat, origin_lon, origin_alt)
az_el_list = GNSS.compute_azel_positions(neu_list)
sat_in_view = GNSS.find_sat_in_view(az_el_list)
sat_total = GNSS.find_sat_total(az_el_list)
print("Satellite total:", len(sat_total))
print("Satellite in View:", len(sat_in_view))
print("Predicted PDOP:", pdop)
