
import os
import requests
import schedule
import time
import os
import requests
from datetime import datetime

# URL to fetch TLE data
def fetch_tle_data():
    # Get the current time
    current_time = datetime.now()
    print(f"Fetching TLE data at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch TLE data
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle"
    output_folder = "TLE_Data"
    output_file = "TLE_Data.txt"

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)

    response = requests.get(url)
    if response.status_code == 200:
        tle_data = response.text.splitlines()
        formatted_tle_data = []
        for i in range(0, len(tle_data) - 2, 3):
            line1 = tle_data[i + 1].strip()
            line2 = tle_data[i + 2].strip()
            formatted_tle_data.append(f"{tle_data[i]}")
            formatted_tle_data.append(f"{line1}")
            formatted_tle_data.append(f"{line2}")

        with open(output_path, "w") as file:
            file.write("\n".join(formatted_tle_data) + "\n")
        print(f"TLE data has been saved to '{output_path}' {current_time.strftime('%Y-%m-%d at %H:%M:%S')}.")
    else:
        print(f"Failed to retrieve TLE data. HTTP Status Code: {response.status_code}")

# Prompt the user for confirmation
def fetch_confirmation():
    current_time = datetime.now()
    while True:
        user_input = input(f"Do you want to fetch the TLE data? Current time {current_time.strftime('%Y-%m-%d at %H:%M:%S')} (yes/no): ").strip().lower()
        if user_input in ["yes", "y"]:
            fetch_tle_data()
            print("Fetch data Done") 
            break
        elif user_input in ["no", "n"]:
            print("Fetch data cancelled") 
            break        
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
        
fetch_confirmation()