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

    # Split the text into lines and parse each line for waypoints
    for line in waypoint_data.splitlines():
        parts = line.split()  # Split by whitespace
        if len(parts) >= 5:  # Ensure the line has enough data (name + coordinates)
            name = parts[0]  # First element is the waypoint name
            latitude = parts[3].replace("N", "").replace("&deg;", "").strip()  # Extract latitude
            longitude = parts[4].replace("E", "").replace("&deg;", "").strip()  # Extract longitude
            waypoints.append({"name": name, "latitude": latitude, "longitude": longitude})

    # Output the extracted waypoints
    for wp in waypoints:
        print(f"Name: {wp['name']}, Latitude: {wp['latitude']}, Longitude: {wp['longitude']}")

else:
    print("No <pre> tag found in the HTML!")
