# Import necessary packages
import psycopg2
from pymongo import MongoClient


# import pandas as pd
# import json
# import geopandas as gpd
# from shapely.geometry import mapping

# Connection to PostgreSQL DB and fetch data for state selected
def get_all_listings(state):
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        host="",
        port='',
        dbname="",
        user="",
        password="")
    print("Connected to the PostgreSQL database.")

    # Create a cursor from the connection
    cur = conn.cursor()

    query = """ SELECT l.id, l.name, l.host_id, l.description, l.latitude, l.longitude, 
                       l.property_type, l.accommodates, l.bedrooms, l.amenities, l.price, 
                       l.minimum_nights, l.maximum_nights, n.neighborhood_group, n.neighborhood
                FROM listings l, neighborhoods n
                WHERE l.neighborhood_id = n.id AND n.state = %s 
            """

    cur.execute(query, (state,))
    result = cur.fetchall()
    print(f"Records for {state} have been successfully fetched.")

    # Close the cursor and the database connection
    cur.close()
    conn.close()
    print("PostgreSQL database connection closed.")

    return result


# Dropdown list for New York
NY_Boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]


# Fetch Neighborhoods from the PostresDB

def get_neighborhoods(NY_Borough):
    # Create a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="",
        port='',
        dbname="",
        user="",
        password=""
    )

    # Create a cursor object
    cur = conn.cursor()

    query2 = """SELECT neighborhood
               FROM neighborhoods
               WHERE neighborhood_group = %s
               """
    cur.execute(query2, (NY_Borough,))

    # Fetch all the rows
    neighborhoods = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return [item[0] for item in neighborhoods]


def app():
    neighborhoods = get_neighborhoods()


# # Connect to MongoDB
# print('Connecting to the MongoDB...')
# client = MongoClient("mongodb://localhost:27017/")
# db = client[""]
# collection = db["ssdsfsdsssss"]
# print("Connected to the MongoDB.")
# print("Neighborhoods collection created.")


def mongo_connect():
    try:
        print('Connecting to the MongoDB...')
        client = MongoClient("")
        db = client[""]
        collection = db[""]
        print("Connected to the MongoDB.")
        print("Neighborhoods collection created.")
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


# 1-Filter to specific neighborhood_group
def filter_neighborhood_group(listing_rows, neighborhood):
    neighborhood = str.lower(neighborhood)
    print(f"Records for {neighborhood} has been been successfully fetched.")
    return list(row for row in listing_rows if row[13].lower() == neighborhood)


# Get geojson records by state
def get_geojson(state):
    client = MongoClient("")
    db = client[""]
    collection = db[""]
    data = collection.find({"state": state})
    return list(f for f in data if 'geometry' in f)


# Filtering for prices
def filter_price(listing_rows, min_price, max_price):
    return list(row for row in listing_rows if min_price <= row[10] <= max_price)


# Insert geojson data into MongoDB for the first map

# def insert_geo_info(file_path, state):
#     geo_data = gpd.read_file(file_path)
#
#     documents = []
#     for _, row in geo_data.iterrows():
#         geom = mapping(row['geometry'])  # Convert geometry to a format MongoDB understands
#         properties = row.drop('geometry').to_dict()
#         document = {'type': 'Feature', 'properties': properties, 'geometry': geom, 'state': state}
#         documents.append(document)
#     print(f"Inserting geojson data for {state}...")
#     # Insert documents into MongoDB
#     collection.insert_many(documents)
#     print(f"Geojson data successfully inserted for {state}...")
#
#
# insert_geo_info('usa-2/New York City/neighbourhoods.geojson', "NY")
# insert_geo_info('usa-2/Hawaii/neighbourhoods.geojson', "HI")


# Insert geojson data into MongoDB for the second map

# db = client.rentdevous_Listings
# db.create_collection("neighbourhood_Map2")
# collection = db['neighbourhood_Map2']
#
#
# file_path = 'NYC_neighbourhoods.geojson'
# geo_data = gpd.read_file(file_path)
#
#
# # Convert the GeoDataFrame to a list of dictionaries for MongoDB
# documents = []
# for _, row in geo_data.iterrows():
#     geom = mapping(row['geometry'])  # Convert geometry to a format MongoDB understands
#     properties = row.drop('geometry').to_dict()
#     document = {'type': 'Feature', 'properties': properties, 'geometry': geom}
#     documents.append(document)

# # Insert documents into MongoDB
# collection.insert_many(documents)


# Grab records for NY and Hawaii in preparation for their button clicks
NY_staging = get_all_listings("NY")
HW_staging = get_all_listings("HI")
