import requests

# POST request URL
url = "https://rfinder.asalink.net/free/autoroute_rtx.php"  # Replace with the actual endpoint

# Define headers (check in the network tab)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",  # Likely used for form data
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# Define the payload
payload = {
    "id1": "VTBS",
    "ic1": "",
    "id2": "WSSS",
    "ic2": "",
    "minalt": "FL330",
    "maxalt": "FL370",
    "lvl": "B",
    "dbid": "2412",
    "usesid": "Y",
    "usestar": "Y",
    "easet": "Y",
    "rnav": "Y",
    "nats": "R",
    "k": "405324820"
}

# Send the POST request
response = requests.post(url, headers=headers, data=payload)

# Save the response content to a file
if response.status_code == 200:
    # Save the raw HTML to a file
    with open("F:\\Project_RAIM\\Pre-Project\\data\\routefinder_response.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Response saved to 'routefinder_response.html'")
else:
    print(f"Request failed with status code: {response.status_code}")