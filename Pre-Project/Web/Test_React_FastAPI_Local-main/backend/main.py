from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
from pydantic import BaseModel
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

app = FastAPI()

# Allow React frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to match your frontend's domain
    allow_methods=["*"],
    allow_headers=["*"],
)

cred = credentials.Certificate("data/test-raim-firebase-adminsdk-q50cn-65404c64e3.json")
app_db = firebase_admin.initialize_app(cred)
db = firestore.Client(project="test-raim") 


def read_locations_from_csv(file_path):
    locations = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for idx, row in enumerate(csv_reader, start=1):
            locations.append({
                "id": idx,
                "latitude": float(row["Latitude"]),
                "longitude": float(row["Longitude"]),
                "name": row["Name"]
            })
    return locations

# Sample locations: List of dictionaries with latitude and longitude
locations = read_locations_from_csv('data/extracted_waypoints.csv')

class FlightData(BaseModel):
    departure: str
    destination: str
    time: str

@app.get("/locations")
def get_locations():
    return locations

@app.post("/submit")
def submit_flight_data(data: FlightData):
    # Process the submitted data here
    print(f"Received data: {data}")
    process_data(data)
    return {"message": "Data received successfully"}

@app.get("/firestore-data")
def get_firestore_data():
    docs = db.collection('waypoints').stream()
    data = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['name'] = doc.id  # Ensure 'name' field is included
        data.append(doc_dict)
    return data

def process_data(data: FlightData):
    # Function to process the data
    print(f"Processing data: {data}")
    # Add your processing logic here

