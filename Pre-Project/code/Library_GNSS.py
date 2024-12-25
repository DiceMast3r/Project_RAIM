from sgp4.api import Satrec, jday
import numpy as np
import requests
import csv


def fetch_tle_data_txt(file_path):
    url = "https://celestrak.com/NORAD/elements/gp.php?GROUP=gps-ops"
    response = requests.get(url)
    if response.status_code == 200:
        tle_data = "\n".join(
            line for line in response.text.splitlines() if line.strip()
        )
        with open(file_path, "w") as file:
            file.write(tle_data)
        return tle_data
    else:
        print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
        return None


# Constants
a = 6378.137  # Earth's equatorial radius in km
f = 1 / 298.257223563  # Flattening factor
e2 = f * (2 - f)  # Square of eccentricity


def eci_to_ecef(r, jd, fr):
    """
    Convert ECI coordinates to ECEF coordinates.
    """
    # Calculate the Greenwich Sidereal Time (GST)
    t = (jd - 2451545.0) / 36525.0  # Julian centuries from J2000.0
    GMST = (
        280.46061837
        + 360.98564736629 * (jd + fr - 2451545.0)
        + 0.000387933 * t**2
        - (t**3) / 38710000.0
    )
    GMST = GMST % 360.0

    theta = np.radians(GMST)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Rotation matrix from ECI to ECEF
    R = np.array([[cos_theta, sin_theta, 0], [-sin_theta, cos_theta, 0], [0, 0, 1]])

    r_ecef = np.dot(R, r)
    return r_ecef


def latlon_to_ecef(lat, lon, alt=0):
    """
    Convert latitude, longitude, and altitude to ECEF coordinates.

    Parameters:
        lat (float): Latitude in degrees.
        lon (float): Longitude in degrees.
        alt (float, optional): Altitude in meters above the WGS84 ellipsoid. Default is 0.

    Returns:
        tuple: A tuple (x, y, z) representing ECEF coordinates in meters.
    """
    # WGS84 ellipsoid constants
    a = 6378137.0  # semi-major axis in meters
    e2 = 6.69437999014e-3  # square of eccentricity

    # Convert latitude and longitude to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Calculate the prime vertical radius of curvature
    N = a / np.sqrt(1 - e2 * np.sin(lat_rad) ** 2)

    # Calculate ECEF coordinates
    x = (N + alt) * np.cos(lat_rad) * np.cos(lon_rad)
    y = (N + alt) * np.cos(lat_rad) * np.sin(lon_rad)
    z = (N * (1 - e2) + alt) * np.sin(lat_rad)

    return x, y, z


def ecef_to_latlon(r_ecef):
    """
    Convert ECEF coordinates to geodetic latitude, longitude, and altitude.
    """
    x, y, z = r_ecef
    lon = np.arctan2(y, x)

    p = np.sqrt(x**2 + y**2)
    lat = np.arctan2(z, p * (1 - e2))
    lat_prev = 0

    # Iteratively compute latitude
    while abs(lat - lat_prev) > 1e-10:
        lat_prev = lat
        N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)
        lat = np.arctan2(z + e2 * N * np.sin(lat), p)

    N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)
    alt = p / np.cos(lat) - N

    lat = np.degrees(lat)
    lon = np.degrees(lon)
    return lat, lon, alt


def ECEF_to_NEU(x, y, z, lat, lon, height):
    """
    Convert ECEF coordinates to NEU coordinates.

    Parameters:
    ecef_coords : tuple
        ECEF coordinates (X, Y, Z) in kilometers.
    ref_coords : tuple
        Reference geodetic coordinates (latitude, longitude, height) in degrees and meters.

    Returns:
    neu_coords : tuple
        NEU coordinates (North, East, Up) in kilometers.
    """
    # Extract ECEF coordinates
    X, Y, Z = x, y, z
    X = X * 1000 # Convert to meters
    Y = Y * 1000
    Z = Z * 1000

    # Extract reference geodetic coordinates (latitude, longitude in degrees)
    lat_ref, lon_ref, h_ref = lat, lon, height

    # Convert latitude and longitude to radians
    lat_ref_rad = np.radians(lat_ref)
    lon_ref_rad = np.radians(lon_ref)

    # Compute the rotation matrix from ECEF to NEU
    R = np.array([
        [-np.sin(lat_ref_rad) * np.cos(lon_ref_rad), -np.sin(lat_ref_rad) * np.sin(lon_ref_rad), np.cos(lat_ref_rad)],
        [-np.sin(lon_ref_rad), np.cos(lon_ref_rad), 0],
        [np.cos(lat_ref_rad) * np.cos(lon_ref_rad), np.cos(lat_ref_rad) * np.sin(lon_ref_rad), np.sin(lat_ref_rad)]
    ])

    # Reference position in ECEF (X_ref, Y_ref, Z_ref)
    a = 6378137.0  # Earth's semi-major axis (meters)
    f = 1 / 298.257223563  # Earth's flattening
    e2 = 2 * f - f ** 2  # Square of eccentricity

    # Compute N (radius of curvature in the prime vertical)
    N = a / np.sqrt(1 - e2 * np.sin(lat_ref_rad) ** 2)

    X_ref = (N + h_ref) * np.cos(lat_ref_rad) * np.cos(lon_ref_rad)
    Y_ref = (N + h_ref) * np.cos(lat_ref_rad) * np.sin(lon_ref_rad)
    Z_ref = (N * (1 - e2) + h_ref) * np.sin(lat_ref_rad)

    # Compute the difference in ECEF coordinates
    delta_ecef = np.array([X - X_ref, Y - Y_ref, Z - Z_ref])

    # Compute NEU coordinates
    neu_coords = R @ delta_ecef # @ = Matrix multiplication
    # Convert to kilometers
    neu_coords = neu_coords / 1000

    return tuple(neu_coords)


def NEU_to_AZEL(n, e, u):
    """
    Convert NEU coordinates to Azimuth and Elevation.

    Parameters:
    neu_coords : tuple
        NEU coordinates (North, East, Up) in meters.

    Returns:
    azimuth : float
        Azimuth angle in degrees.
    elevation : float
        Elevation angle in degrees.
    """
    # Extract NEU components
    N, E, U = n, e, u

    # Compute Azimuth (in radians)
    azimuth_rad = np.arctan2(E, N)
    azimuth = np.degrees(azimuth_rad)
    if azimuth < 0:
        azimuth += 360

    # Compute Elevation (in radians)
    horizontal_distance = np.sqrt(N**2 + E**2)
    elevation_rad = np.arctan2(U, horizontal_distance)
    elevation = np.degrees(elevation_rad)

    return azimuth, elevation


def read_tle_file(filename):
    """
    Read TLE data from a file and return a list of satellite objects.
    """
    satellites = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            line0 = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            satellite = Satrec.twoline2rv(line1, line2)
            satellites.append((line0, satellite))
    return satellites


def compute_positions(satellites, year, month, day, hour, minute, second):
    """
    Compute the position of each satellite at the given date and time.
    """
    jd, fr = jday(year, month, day, hour, minute, second)
    results = []
    for name, satellite in satellites:
        e, r, v = satellite.sgp4(jd, fr)
        if e == 0:
            r_ecef = eci_to_ecef(r, jd, fr)
            lat, lon, alt = ecef_to_latlon(r_ecef)
            results.append((name, lat, lon, alt))
        else:
            results.append((name, None, None, None))
    return results


def compute_positions_ecef(satellites, year, month, day, hour, minute, second):
    """
    Compute the position of each satellite at the given date and time.
    """
    jd, fr = jday(year, month, day, hour, minute, second)
    results = []
    for name, satellite in satellites:
        e, r, v = satellite.sgp4(jd, fr)
        if e == 0:
            r_ecef = eci_to_ecef(r, jd, fr)
            results.append((name, r_ecef[0], r_ecef[1], r_ecef[2]))
        else:
            results.append((name, None, None, None))
    return results


def compute_positions_neu(ecef_file, origin_lat, origin_lon, origin_alt):
    """
    Compute the local North-East-Up (NEU) coordinates of each satellite.
    """
    positions = []
    with open(ecef_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            sat_id, x, y, z = row[0], float(row[1]), float(row[2]), float(row[3])
            neu = ECEF_to_NEU(x, y, z, origin_lat, origin_lon, origin_alt)
            positions.append((sat_id, neu[0], neu[1], neu[2]))
    return positions

def compute_positions_neu_direct(ecef_list, origin_lat, origin_lon, origin_alt):
    """
    Compute the local North-East-Up (NEU) coordinates of each satellite.
    """
    positions = []
    for sat_id, x, y, z in ecef_list:
        neu = ECEF_to_NEU(x, y, z, origin_lat, origin_lon, origin_alt)
        positions.append((sat_id, neu[0], neu[1], neu[2]))
    return positions


def compute_positions_azel(neu_file):
    """
    Compute the Azimuth-Elevation (AZEL) angles of each satellite.
    """
    positions = []
    with open(neu_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            sat_id, n, e, u = row[0], float(row[1]), float(row[2]), float(row[3])
            az, el = NEU_to_AZEL(n, e, u)
            positions.append((sat_id, az, el))
    return positions

def compute_positions_azel_direct(neu_list):
    """
    Compute the Azimuth-Elevation (AZEL) angles of each satellite.
    """
    positions = []
    for sat_id, n, e, u in neu_list:
        az, el = NEU_to_AZEL(n, e, u)
        positions.append((sat_id, az, el))
    return positions


def save_positions_to_file(
    positions, output_filename, year, month, day, hour, minute, second
):
    """
    Save the computed positions to a CSV file.
    """
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = [
            "Satellite",
            "Latitude",
            "Longitude",
            "Altitude",
            "Year",
            "Month",
            "Day",
            "Hour",
            "Minute",
            "Second",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, lat, lon, alt in positions:
            if lat is not None:
                writer.writerow(
                    {
                        "Satellite": name,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Altitude": alt,
                        "Year": year,
                        "Month": month,
                        "Day": day,
                        "Hour": hour,
                        "Minute": minute,
                        "Second": second,
                    }
                )
            else:
                writer.writerow(
                    {
                        "Satellite": name,
                        "Latitude": "Error",
                        "Longitude": "Error",
                        "Altitude": "Error",
                        "Year": year,
                        "Month": month,
                        "Day": day,
                        "Hour": hour,
                        "Minute": minute,
                        "Second": second,
                    }
                )


def save_position_to_file_ecef(
    positions, output_filename, year, month, day, hour, minute, second
):
    """
    Save the computed ECEF positions to a CSV file.
    """
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = [
            "Satellite",
            "X",
            "Y",
            "Z",
            "Year",
            "Month",
            "Day",
            "Hour",
            "Minute",
            "Second",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, x, y, z in positions:
            if x is not None:
                writer.writerow(
                    {
                        "Satellite": name,
                        "X": x,
                        "Y": y,
                        "Z": z,
                        "Year": year,
                        "Month": month,
                        "Day": day,
                        "Hour": hour,
                        "Minute": minute,
                        "Second": second,
                    }
                )
            else:
                writer.writerow(
                    {
                        "Satellite": name,
                        "X": "Error",
                        "Y": "Error",
                        "Z": "Error",
                        "Year": year,
                        "Month": month,
                        "Day": day,
                        "Hour": hour,
                        "Minute": minute,
                        "Second": second,
                    }
                )


def save_positions_to_file_neu(positions, output_filename, origin_lat, origin_lon, origin_alt):
    """
    Save the computed NEU positions to a CSV file.
    """
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = ["Satellite", "North", "East", "Up", "Origin Latitude", "Origin Longitude", "Origin Altitude"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, n, e, u in positions:
            writer.writerow(
                {
                    "Satellite": name,
                    "North": n,
                    "East": e,
                    "Up": u,
                    "Origin Latitude": origin_lat,
                    "Origin Longitude": origin_lon,
                    "Origin Altitude": origin_alt
                }
            )

def save_positions_to_file_azel(positions, output_filename, origin_lat, origin_lon):
    """
    Save the computed AZ,EL to a CSV file.
    """
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = ["Satellite", "Azimuth", "Elevation", "Origin Latitude", "Origin Longitude"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, az, el in positions:
            writer.writerow(
                {
                    "Satellite": name,
                    "Azimuth": az,
                    "Elevation": el,
                    "Origin Latitude": origin_lat,
                    "Origin Longitude": origin_lon
                }
            )


def calculate_distance_and_unit_vector(sat, rec):
    dist = np.sqrt(np.sum((sat - rec) ** 2))
    unit_vector = (sat - rec) / dist
    return unit_vector

def calculate_g_matrix(sat_position, rec_position):
    G = []
    for sat in sat_position:
        unit_vector = calculate_distance_and_unit_vector(np.array(sat), np.array(rec_position))
        G.append(unit_vector)
    return np.array(G)

def calculate_pdop(G):
    G_transpose = G.T
    GTG = np.dot(G_transpose, G)
    GIN = np.linalg.inv(GTG)
    GIN_MID = [GIN[i][i] for i in range(len(GIN))]
    PDOP = np.sqrt(np.sum(GIN_MID))
    return PDOP

def calculate_pdop_from_pos(sat_position, rec_position):
    G = calculate_g_matrix(sat_position, rec_position)
    PDOP = calculate_pdop(G)
    return PDOP

def init_sat_obj(tle_file_path):
    sat_obj = read_tle_file(tle_file_path)
    #print("TLE data read from file.")
    return sat_obj

def compute_ecef_positions(tle_file_path, year, month, day, hour, minute, second):
    #fetch_tle_data_txt(tle_file_path)
    ini_sat_obj = init_sat_obj(tle_file_path)
    position_data_ecef = compute_positions_ecef(ini_sat_obj, year, month, day, hour, minute, second)
    return position_data_ecef

def compute_neu_positions(ecef_list, origin_lat, origin_lon, origin_alt):
    position_NEU = compute_positions_neu_direct(ecef_list, origin_lat, origin_lon, origin_alt)
    return position_NEU

def compute_azel_positions(neu_list):
    az_el = compute_positions_azel_direct(neu_list)
    return az_el

def extract_ecef_pos(ecef_list):
    ecef_pos = []
    for i in range(len(ecef_list)):
        ecef_pos.append(ecef_list[i][1:4])
    return ecef_pos

def cal_pdop(sat_position, rec_position):
    G = []
    GIN_MID = []
    rec_position = np.array(rec_position, dtype=np.float64)  # Ensure rec_position is float64
    for sat in sat_position:
        sat = np.array(sat, dtype=np.float64)  # Ensure sat is float64
        dist = np.sqrt(np.sum((sat - rec_position) ** 2))
        unit_vector = (sat - rec_position) / dist
        G.append(unit_vector)
    G = np.array(G)
    G_transpose = G.T
    GTG = np.dot(G_transpose, G)
    GIN = np.linalg.inv(GTG)
    for i in range(len(GIN)):
        GIN_MID.append(GIN[i][i])
    PDOP = np.sqrt(np.sum(GIN_MID))

    return PDOP

def find_sat_in_view(az_el_list):
    sat_in_view = []
    for i in range(len(az_el_list)):
        if az_el_list[i][2] > 10:
            sat_in_view.append(az_el_list[i])
    return sat_in_view

def find_sat_total(az_el_list):
    sat_total = []
    for i in range(len(az_el_list)):
        sat_total.append(az_el_list[i])
    return sat_total

def az_el_to_neu(az, el, r):
    """
    Convert azimuth, elevation, and range to NEU coordinates.

    Parameters:
        az (float): Azimuth angle in degrees (clockwise from North).
        el (float): Elevation angle in degrees.
        r (float): Range (distance to target) in meters.

    Returns:
        tuple: A tuple (n, e, u) representing North, East, Up coordinates in meters.
    """
    # Convert azimuth and elevation to radians
    az_rad = np.radians(az)
    el_rad = np.radians(el)

    # Calculate NEU components
    n = r * np.cos(el_rad) * np.cos(az_rad)
    e = r * np.cos(el_rad) * np.sin(az_rad)
    u = r * np.sin(el_rad)

    return n, e, u

def neu_to_ecef(n, e, u, lat_ref, lon_ref, ecef_ref):
    """
    Convert NEU coordinates to ECEF coordinates.

    Parameters:
        n (float): North component in meters.
        e (float): East component in meters.
        u (float): Up component in meters.
        lat_ref (float): Reference latitude in degrees.
        lon_ref (float): Reference longitude in degrees.
        ecef_ref (tuple): Reference ECEF coordinates (x, y, z) in meters.

    Returns:
        tuple: A tuple (x, y, z) representing ECEF coordinates in meters.
    """
    # Convert reference latitude and longitude to radians
    lat_ref_rad = np.radians(lat_ref)
    lon_ref_rad = np.radians(lon_ref)

    # Compute the rotation matrix from NEU to ECEF
    R = np.array([
        [-np.sin(lat_ref_rad) * np.cos(lon_ref_rad), -np.sin(lon_ref_rad), np.cos(lat_ref_rad) * np.cos(lon_ref_rad)],
        [-np.sin(lat_ref_rad) * np.sin(lon_ref_rad),  np.cos(lon_ref_rad), np.cos(lat_ref_rad) * np.sin(lon_ref_rad)],
        [ np.cos(lat_ref_rad),                       0,                  np.sin(lat_ref_rad)]
    ])

    # Convert NEU to ECEF
    neu = np.array([n, e, u])
    ecef_offset = R.T @ neu  # Transpose for proper transformation
    ecef = ecef_ref + ecef_offset

    return tuple(ecef)


def Az_El_to_ECEF(az_el_list, origin_lat, origin_lon, origin_alt, r=20200000):
    ECEF_result = []
    r = r - origin_alt
    for i in range(len(az_el_list)):
        n, e, u = az_el_to_neu(az_el_list[i][1], az_el_list[i][2], r)
        ECEF = neu_to_ecef(n, e, u, origin_lat, origin_lon, origin_alt)
        ECEF_result.append(ECEF)
        
    return ECEF_result
    