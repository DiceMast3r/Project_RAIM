import numpy as np
import Library_GNSS as GNSS

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


# Input data (Azimuth, Elevation in degrees, Range in meters)
data = [
    ('GPS BIIR-11 (PRN 19)', np.float64(320.71016008931565), np.float64(33.667575375415424)),
    ('GPS BIIRM-1 (PRN 17)', np.float64(0.2991301166534506), np.float64(37.654427351014775))
]

# Reference location (latitude, longitude, and ECEF)
reference_lat = 52.5200  # Berlin latitude in degrees
reference_lon = 13.4050  # Berlin longitude in degrees
reference_alt = 34.0  # Approximate altitude in meters above sea level
reference_ecef = GNSS.latlon_to_ecef(reference_lat, reference_lon, reference_alt)

# Define an arbitrary range (distance to satellite)
range_to_satellite = 20200000.0  # Approximate range to GPS satellites in meters

# Convert each Az, El to ECEF
ecef_results = []
for name, az, el in data:
    # Step 1: Convert Azimuth/Elevation to NEU
    neu_coords = az_el_to_neu(az, el, range_to_satellite)
    
    # Step 2: Convert NEU to ECEF
    ecef_coords = neu_to_ecef(*neu_coords, reference_lat, reference_lon, reference_ecef)
    
    ecef_results.append((name, ecef_coords))

# Print results
for name, ecef in ecef_results:
    print(f"{name} ECEF Coordinates: {ecef}")
