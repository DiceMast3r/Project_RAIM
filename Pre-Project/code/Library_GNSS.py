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


def ECEF_to_NEU(x, y, z, lat, lon):
    """
    Convert ECEF coordinates to local North-East-Up (NEU) coordinates.
    """
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    cos_lat = np.cos(lat_rad)
    sin_lat = np.sin(lat_rad)
    cos_lon = np.cos(lon_rad)
    sin_lon = np.sin(lon_rad)

    # Rotation matrix from ECEF to ENU
    R = np.array(
        [
            [-sin_lon, cos_lon, 0],
            [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
            [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat],
        ]
    )

    r = np.array([x, y, z])
    neu = np.dot(R, r)
    return neu


def NEU_to_AZEL(n, e, u):
    """
    Convert local North-East-Up (NEU) coordinates to Azimuth-Elevation (AZEL) angles.
    """
    x, y, z = n, e, u
    r = np.sqrt(x**2 + y**2 + z**2)
    az = np.arctan2(x, y)
    el = np.arcsin(z / r)
    return np.degrees(az), np.degrees(el)


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


def compute_positions_neu(ecef_file, origin_lat, origin_lon):
    """
    Compute the local North-East-Up (NEU) coordinates of each satellite.
    """
    positions = []
    with open(ecef_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            sat_id, x, y, z = row[0], float(row[1]), float(row[2]), float(row[3])
            neu = ECEF_to_NEU(x, y, z, origin_lat, origin_lon)
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


def save_positions_to_file_neu(positions, output_filename, origin_lat, origin_lon):
    """
    Save the computed NEU positions to a CSV file.
    """
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = ["Satellite", "North", "East", "Up", "Origin Latitude", "Origin Longitude"]
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
                    "Origin Longitude": origin_lon
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
