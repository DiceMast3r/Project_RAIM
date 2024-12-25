
from skyfield.api import Topos, load, wgs84
from skyfield.sgp4lib import EarthSatellite
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal.windows import tukey
import datetime
import requests
import re
import os

def read_tle_file(file_path):
    tle_data = {}
    try:
        with open(file_path, "r") as tle_file:
            lines = tle_file.readlines()

            # Parse the file line-by-line into a dictionary
            for i in range(0, len(lines) - 2, 3):
                name = lines[i].strip()
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()

                # Use a regular expression to extract PRN numbers (e.g., PRN 13)
                match = re.search(r"PRN (\d+)", name)
                if match:
                    prn_number = int(match.group(1))
                    key = f"G{prn_number:02d}"  # Format PRN number as G01, G13, etc.

                    # Add the TLE pair to the dictionary
                    tle_data[key] = [line1, line2]

        return tle_data

    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def skyplot(lat, lon, TLE_Data,):
    FONTSIZE=10
    # Create an observer location
    ts = load.timescale()
    time = ts.now()
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)

    # Initialize satellite objects and filter out PRN 01
    satellite_objects = {
        sat: EarthSatellite(TLE_Data[sat][0], TLE_Data[sat][1], sat, ts)
        for sat in TLE_Data
        #if int(sat[1:3]) != 1  # Exclude PRN 01
    }

    # Create the plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 90)  # Altitude 0° (horizon) to 90° (zenith)

    # Plot satellites
    for sat in satellite_objects:
        difference = satellite_objects[sat] - observer
        topocentric = difference.at(time)
        alt, az, distance = topocentric.altaz()

        if alt.degrees > 0:  # Only plot if above the horizon
            r = 90 - alt.degrees
            theta = np.radians(az.degrees)
            ax.plot(theta, r, 'o', color='black')
            ax.text(theta, r, f'{sat}', fontsize=FONTSIZE, ha='right', va='bottom')

    # Add azimuth angle labels
    azimuth_angles = np.arange(0, 360, 30)  # Azimuth angles every 30°
    for angle in azimuth_angles:
        theta = np.radians(angle)
        ax.text(
            theta, 95,  # Place slightly outside the maximum range for labels
            f'{angle}°', fontsize=FONTSIZE, ha='center', va='center', color='blue'
        )

    # Add grid lines
    radial_grid_angles = np.linspace(0, 2 * np.pi, 360)  # Fine grid for circles
    for radius in [15, 30, 45, 60, 75, 90]:  # Altitude rings
        ax.plot(radial_grid_angles, [90 - radius] * len(radial_grid_angles), '--', color='gray', linewidth=0.5)

    azimuth_grid_angles = np.arange(0, 360, 10)  # Grid every 10° azimuth
    for angle in azimuth_grid_angles:
        theta = np.radians(angle)
        ax.plot([theta, theta], [0, 90], '--', color='gray', linewidth=0.5)

    # Customize plot appearance
    ax.set_rmax(90)
    ax.set_rticks([0, 15, 30, 45, 60, 75, 90])  # Altitude rings
    ax.set_rlabel_position(0)  # Move radial labels
    ax.set_rgrids([0, 15, 30, 45, 60, 75, 90], labels=["90", "75", "60", "45", "30", "15", ""], fontsize=FONTSIZE)
    ax.grid(True)  # Enable the default grid lines
    ax.set_thetalim([0, 2 * np.pi])
    ax.set_thetagrids(np.rad2deg(np.linspace(0, 2 * np.pi, 5)[1:]), labels=["E", "S", "W", "N"], fontsize=FONTSIZE, va='center',color='blue', y=0.1)

    # Show the plot
    plt.show()

