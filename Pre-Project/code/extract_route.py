import re
from bs4 import BeautifulSoup

""" This script extracts waypoints from a HTML file containing route data. into a CSV file. """


# Load the HTML file
with open("D:\\Project_RAIM\\Pre-Project\\data\\routefinder_response.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "lxml")

# Locate the <pre> tag containing the waypoint data
pre_tag = soup.find("pre")
if pre_tag:
    waypoint_data = pre_tag.text.strip()  # Extract raw text

    waypoints = []  # List to store extracted waypoints

    # Debugging: Print the raw text to verify format
    print("Raw Data from <pre> tag:\n")
    print(waypoint_data)
    print("\nParsing Waypoints...\n")

    # Updated Regex pattern for DMS format
    dms_pattern = re.compile(
        r"(?P<lat_dir>[NS])(?P<lat_deg>\d{1,2})°(?P<lat_min>\d{1,2})'(?P<lat_sec>\d{1,2}\.\d+)?\"?\s+"
        r"(?P<lon_dir>[EW])(?P<lon_deg>\d{1,3})°(?P<lon_min>\d{1,2})'(?P<lon_sec>\d{1,2}\.\d+)?\"?"
    )

    # Split the text into lines and parse each line for waypoints
    for line in waypoint_data.splitlines():
        #print(f"Processing Line: {line}")  # Debugging: Print each line

        # Match latitude and longitude in DMS format
        match = dms_pattern.search(line)
        if match:
            # Extract the DMS components
            lat_dir = match.group("lat_dir")
            lat_deg = int(match.group("lat_deg"))
            lat_min = int(match.group("lat_min"))
            lat_sec = float(match.group("lat_sec")) if match.group("lat_sec") else 0

            lon_dir = match.group("lon_dir")
            lon_deg = int(match.group("lon_deg"))
            lon_min = int(match.group("lon_min"))
            lon_sec = float(match.group("lon_sec")) if match.group("lon_sec") else 0

            # Convert DMS to decimal degrees
            latitude = lat_deg + lat_min / 60 + lat_sec / 3600
            if lat_dir == "S":
                latitude = -latitude

            longitude = lon_deg + lon_min / 60 + lon_sec / 3600
            if lon_dir == "W":
                longitude = -longitude

            # Extract waypoint name (assume it's the first word in the line)
            parts = line.split()
            name = parts[0]

            # Append to waypoints list
            waypoints.append({
                "name": name,
                "latitude": round(latitude, 8),  # Round to 6 decimal places
                "longitude": round(longitude, 8)  # Round to 6 decimal places
            })
            #print(f"Extracted Waypoint: {name}, Lat: {latitude}, Lon: {longitude}")  # Debugging
        else:
            print(f"Skipping Line: {line} (No valid coordinates found)")  # Log skipped lines

    # Output the extracted waypoints
    print("\nExtracted Waypoints:")
    for wp in waypoints:
        print(f"Name: {wp['name']}, Latitude: {wp['latitude']}, Longitude: {wp['longitude']}")     
else:
    print("No <pre> tag found in the HTML content")

# Save the extracted waypoints to a csv file
with open("D:\\Project_RAIM\\Pre-Project\\data\\extracted_waypoints.csv", "w", newline="") as file:
    # Write the header
    file.write("Name,Latitude,Longitude\n")

    # Write each waypoint as a line in the csv file
    for wp in waypoints:
        file.write(f"{wp['name']},{wp['latitude']},{wp['longitude']}\n")

    print("\nExtracted waypoints saved to 'extracted_waypoints.csv'")

