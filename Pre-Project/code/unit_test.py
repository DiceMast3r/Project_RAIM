import numpy as np

origin_lat = 13.75
origin_lon = 100.50
receiver_alt = 20

def ecef_to_neu(ecef_coords, ref_coords):
    """
    Convert ECEF coordinates to NEU coordinates.

    Parameters:
    ecef_coords : tuple
        ECEF coordinates (X, Y, Z) in meters.
    ref_coords : tuple
        Reference geodetic coordinates (latitude, longitude, height) in degrees and meters.

    Returns:
    neu_coords : tuple
        NEU coordinates (North, East, Up) in meters.
    """
    # Extract ECEF coordinates
    X, Y, Z = ecef_coords

    # Extract reference geodetic coordinates (latitude, longitude in degrees)
    lat_ref, lon_ref, h_ref = ref_coords

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
    neu_coords = R @ delta_ecef

    return tuple(neu_coords)

def neu_to_az_el(neu_coords):
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
    N, E, U = neu_coords

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

# Example usage
if __name__ == "__main__":
    # Example ECEF coordinates (meters)
    ecef_coords = (-12668213.300141417, 23191267.88301844, -464141.21054881474)

    # Reference geodetic coordinates (latitude, longitude in degrees, height in meters)
    ref_coords = (13.75, 100.5, 20.0) 

    neu_coords = ecef_to_neu(ecef_coords, ref_coords)
    print("NEU coordinates:", neu_coords)

    azimuth, elevation = neu_to_az_el(neu_coords)
    print("Azimuth:", azimuth, "degrees")
    print("Elevation:", elevation, "degrees")
