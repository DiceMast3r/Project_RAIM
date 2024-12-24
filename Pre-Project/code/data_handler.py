import Library_GNSS as GNSS
import numpy as np

def compute_satellite_data(year, month, day, hour, minute, second, origin_lat, origin_lon, origin_alt):
    tle_file_path = "F:\\Project_RAIM\\Pre-Project\\data\\TLE.txt"
    
    # Convert UTC+7 to UTC
    hour_utc = hour - 7
    if hour_utc < 0:
        hour_utc += 24
        day -= 1

    ecef_list = GNSS.compute_ecef_positions(
        tle_file_path, year, month, day, hour_utc, minute, second
    )
    neu_list = GNSS.compute_neu_positions(ecef_list, origin_lat, origin_lon, origin_alt)
    az_el_list = GNSS.compute_azel_positions(neu_list)
    sat_in_view = GNSS.find_sat_in_view(az_el_list)
    sat_in_view_ECEF = GNSS.Az_El_to_ECEF(sat_in_view, origin_lat, origin_lon, origin_alt)
    sat_total = GNSS.find_sat_total(az_el_list)
    pdop = (
        GNSS.cal_pdop(
            sat_in_view_ECEF,
            GNSS.latlon_to_ecef(origin_lat, origin_lon, origin_alt),
        )
    )
    
    
    return pdop, len(sat_in_view), len(sat_total)

# Example usage:
# compute_satellite_data(2024, 12, 12, 19, 20, 0, 13.683529, 100.619786, 0)

pdop, sat_view, sat_tot = compute_satellite_data(2024, 12, 22, 19, 25, 0, 13.683529, 100.619786, 0)

