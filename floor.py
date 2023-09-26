import pymongo
import requests
from pymongo import errors

# Initialize MongoDB connection
try:
    client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.6jl6her.mongodb.net/?retryWrites=true&w=majority")
    db = client["testDb"]
    collection = db["testCollection"]
except errors.ConnectionError as e:
    print(f"Error: {str(e)}")


# Function to fetch and update JSON data
def update_mongodb_from_json_url():
    try:
        # Fetch JSON data from a remote URL
        json_url = "https://floor.b-cdn.net/floor.json"
        response = requests.get(json_url)
        new_json_data = response.json()

        # Compare with existing data and update based on layout_id
        for new_item in new_json_data:
            layout_id = new_item["layout_id"]
            existing_item = collection.find_one({"layout_id": layout_id})

            if existing_item:
                # Update the existing document
                collection.update_one({"layout_id": layout_id}, {"$set": new_item})
                print(f"Updated document with layout_id: {layout_id}")
            else:
                # Insert a new document
                collection.insert_one(new_item)
                print(f"Inserted new document with layout_id: {layout_id}")

        print("MongoDB updated with new JSON data.")

    except Exception as e:
        print(f"Error: {str(e)}")

# Call the function to update MongoDB
update_mongodb_from_json_url()
