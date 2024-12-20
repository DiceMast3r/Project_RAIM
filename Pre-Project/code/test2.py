import numpy as np

def geodetic_to_ecef(lat, lon, alt):
    # WGS-84 ellipsiod parameters
    a = 6378137.0  # semi-major axis in meters
    f = 1 / 298.257223563  # flattening
    e2 = 2 * f - f ** 2  # square of eccentricity

    lat = np.radians(lat)
    lon = np.radians(lon)

    N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)

    X = (N + alt) * np.cos(lat) * np.cos(lon)
    Y = (N + alt) * np.cos(lat) * np.sin(lon)
    Z = (N * (1 - e2) + alt) * np.sin(lat)

    return X, Y, Z

# Coordinates of Bangkok
latitude = 13.72782749
longitude = 100.77243502
altitude = 29.385  # in meters

ecef_coords = geodetic_to_ecef(latitude, longitude, altitude)
print("ECEF Coordinates of Bangkok:", ecef_coords)