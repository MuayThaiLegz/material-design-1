
#mongoconnection.py

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.server
from pymongo import MongoClient
import pandas as pd
from io import BytesIO
import re
from functools import lru_cache
import calendar
from data_processing import process_datafile, clean_column_names, identify_datetime_cols, convert_to_datetime, create_features

@anvil.server.callable
def connect_to_mongodb(connString):
    """
    Attempts to connect to MongoDB with the provided connection string.
    Returns a success status and message.
    """
    try:
        client = MongoClient(connString)
        client.admin.command('ping')
        client.close()
        return True, "Connected successfully."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

@anvil.server.callable
def get_verticals(connString):
    """
    Retrieves the list of databases and their collections.
    """
    try:
        client = MongoClient(connString)
        verticals = {db: client[db].list_collection_names() for db in client.list_database_names() if db not in ['admin', 'local', 'config','Modelsdb','dev_db','document_embeddings','Models_evaluation']}
        print(verticals.keys())
        return True, verticals
    except Exception as e:
        return False, f"Failed to get verticals: {str(e)}"


def sanitize_name(name):
    """Sanitize database or collection name."""
    return re.sub(r'[.\s]', '_', name)


import pandas as pd
from io import BytesIO
import re
from pymongo import MongoClient
import anvil.server

@anvil.server.callable
def store_data(db_name, collection_name, file, connString):
    print('Entering')
  
    if not file:
        print("No file provided.")
        return False, "No file provided."
        
    sanitized_db_name = re.sub(r'[.\s]', '_', db_name)
    print(sanitized_db_name)
  
    # Assuming a simple sanitize function or just use the raw name if you trust the source
    sanitized_collection_name = re.sub(r'[.\s]', '_', collection_name)
    print(sanitized_collection_name)

    client = MongoClient(connString)
    db = client[sanitized_db_name]
    collection = db[sanitized_collection_name]
    
    # Read file into DataFrame
    file_like_object = BytesIO(file.get_bytes())
    if file.content_type == 'text/csv':
        df = pd.read_csv(file_like_object)
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file_like_object)
    elif file.content_type == 'application/json':
        df = pd.read_json(file_like_object)
    else:
        client.close()
        return False, "Unsupported file type."

    # If there's data processing needed, call process_datafile here and ensure it's implemented
    
    # Directly converting df to records and inserting into MongoDB
    # df, lat_long_list, numerical_data, numerical_options_list, object_data, object_options_list, main_datetime_col = process_datafile(df)
  
    records = df.to_dict('records')
    collection.insert_many(records)
    client.close()
    return True, f"Data saved successfully in {sanitized_db_name}/{sanitized_collection_name}."

@anvil.server.callable
def get_database_names(connString):
    try:
        # Create a MongoDB client
        client = MongoClient(connString)
        # List database names
        db_nameslist = client.list_database_names()
        db_names = [i for i in db_nameslist if i not in ['Models_evaluation', 'Modelsdb','admin','config','local']]
        # db_names = [i for i in client.list_database_names() if i not in ['Models_evaluation', 'Modelsdb','admin','config','local']]

        return True, db_names
    except Exception as e:
        return False, str(e)

@anvil.server.callable
def get_collection_names(conn_string, db_name):
    try:
        client = MongoClient(conn_string)
        db = client[db_name]
        collection_names = db.list_collection_names()
        client.close()
        return collection_names
    except Exception as e:
        return ["Error: " + str(e)]

@anvil.server.callable
def fetch_collection_data(conn_string, db_name, collection_name):
    try:
        client = MongoClient(conn_string)
        db = client[db_name]
        collection = db[collection_name]
        data = pd.DataFrame(list(collection.find({}, {'_id': False})))  # Assuming you don't want to send MongoDB's _id field to the client
        data = df.to_dict('records')
        columns = df.columns.tolist()    
        client.close()
        return data, columns
    except Exception as e:
        return [{"Error": str(e)}]
      
@anvil.server.callable
def initiate_file_processing(file, db_name, collection_name, connString):
    anvil.server.launch_background_task('store_data', file, db_name, collection_name, connString)
    return "Processing started"
