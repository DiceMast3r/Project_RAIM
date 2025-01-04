import firebase_admin
from firebase_admin import firestore
import csv

def read_waypoints(file_path):
    waypoints = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, latitude, longitude = row
            waypoints.append((name, float(latitude), float(longitude)))
    return waypoints

def read_ecef_positions(file_path):
    ecef_positions = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            ecef_positions.append(((row[0]), float(row[1]), float(row[2]), float(row[3])))
    return ecef_positions

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.Client(project="test-raim") 

'''doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

doc_ref = db.collection("users").document("aturing")
doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})'''


file_path = "F:\\Project_RAIM\\Pre-Project\\data\\extracted_waypoints.csv"
ecef_file = "F:\\Project_RAIM\\Pre-Project\\data\\POS_ECEF.csv"
wp = read_waypoints(file_path)
#print(wp)

ecef = read_ecef_positions(ecef_file)
#print(ecef)

# Add waypoints to Firestore
for index, (name, latitude, longitude) in enumerate(wp):
    indexed_name = f"{index:02d}_{name}"
    doc_ref = db.collection("waypoints").document(indexed_name)
    doc_ref.set({"latitude": latitude, "longitude": longitude, "order": index})

print("Waypoints added to Firestore")

# Add ECEF positions to Firestore under the waypoint "VTBS"
waypoint_name = "00_VTBS"
for index, (name, x, y, z) in enumerate(ecef):
    indexed_name = f"{index:02d}_{name}"
    doc_ref = db.collection("waypoints").document(waypoint_name).collection("ecef_positions").document(indexed_name)
    doc_ref.set({"x": x, "y": y, "z": z, "order": index})
    
print("ECEF positions added to Firestore")




'''users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")'''