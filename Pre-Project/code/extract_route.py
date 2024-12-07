import re
from bs4 import BeautifulSoup

# Load the HTML file (replace 'response.html' with your actual file name)
with open("F:\\Project_RAIM\\Pre-Project\\data\\routefinder_response.html", "r", encoding="utf-8") as file:
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

    # Updated Regex patterns for latitude and longitude (handle degree symbols, decimals, etc.)
    lat_pattern = re.compile(r"N(\d{1,2}(?:\.\d+)?).*?")  # Matches N12.34 or N12°34
    lon_pattern = re.compile(r"E(\d{1,3}(?:\.\d+)?).*?")  # Matches E100.12 or E100°12

    # Split the text into lines and parse each line for waypoints
    for line in waypoint_data.splitlines():
        print(f"Processing Line: {line}")  # Debugging: Print each line

        # Match latitude and longitude using regex
        lat_match = lat_pattern.search(line)
        lon_match = lon_pattern.search(line)

        if lat_match and lon_match:
            # Extract name (first column) and coordinates
            parts = line.split()
            name = parts[0]  # Assume the first column is always the waypoint name
            latitude = lat_match.group(1).replace("°", "").strip()
            longitude = lon_match.group(1).replace("°", "").strip()

            # Append to waypoints list
            waypoints.append({
                "name": name,
                "latitude": latitude,
                "longitude": longitude
            })
            print(f"Extracted Waypoint: {name}, Lat: {latitude}, Lon: {longitude}")  # Debugging
        else:
            print(f"Skipping Line: {line} (No valid coordinates found)")  # Log skipped lines

    # Output the extracted waypoints
    print("\nExtracted Waypoints:")
    for wp in waypoints:
        print(f"Name: {wp['name']}, Latitude: {wp['latitude']}, Longitude: {wp['longitude']}")

else:
    print("No <pre> tag found in the HTML!")
