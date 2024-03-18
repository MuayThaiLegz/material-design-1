
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
    records = df.to_dict('records')
    collection.insert_many(records)
    client.close()
    return True, f"Data saved successfully in {sanitized_db_name}/{sanitized_collection_name}."


# @anvil.server.callable
# def store_data(db_name, collection_name, file, connString):
#     print('Entering')
#     """
#     Stores the data from the uploaded file into the specified MongoDB collection.
#     """
  
#       # Ensure file is not None and has a content_type
#     if not file or not hasattr(file, 'content_type'):
#       print("No file or file type provided.")
#       return False, "No file or file type provided."
      
#     sanitized_db_name = re.sub(r'[.\s]', '_', db_name)
#     print(sanitized_db_name)
  
#     sanitized_collection_name = sanitize_name(collection_name)
#     print(sanitized_collection_name)

#     client = MongoClient(connString)
#     db = client[sanitized_db_name]
#     collection = db[sanitized_collection_name]
    
#     # Read file into DataFrame
#     file_like_object = BytesIO(file.get_bytes())
#     print(file_like_object)
#     if file.content_type == 'text/csv':
#         df = pd.read_csv(file_like_object)
#     elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
#         df = pd.read_excel(file_like_object)
#     elif file.content_type == 'application/json':
#         df = pd.read_json(file_like_object)
#     else:
#         return False, "Unsupported file type."

#     # Process and store the DataFrame
#     processed_df, _, _, _, _, _, _ = process_datafile(df)
#     records = df.to_dict('records')
#     collection.insert_many(records)
#     client.close()
#     return True, f"Data saved successfully in {sanitized_db_name}/{sanitized_collection_name}."

# @anvil.server.callable
# def process_and_load_file(file, connString):
#     try:
#         client = MongoClient(connString)
#         file_like_object = BytesIO(file.get_bytes())
        
#         if file.content_type == 'text/csv':
#             df = pd.read_csv(file_like_object)
#         elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
#             df = pd.read_excel(file_like_object)
#         elif file.content_type == 'application/json':
#             df = pd.read_json(file_like_object)

#         df = process_datafile(df)
#         uploaded_fileName = file.name.rsplit('.', 1)[0]
#         db = client['AnvilVille']
#         collection = db[uploaded_fileName]
#         collection.insert_many(df.to_dict('records'))
#         client.close()
#         return True, f"Data saved successfully in {uploaded_fileName}."
#     except Exception as e:
#         return False, f"Failed to process file: {str(e)}"
      
@anvil.server.callable
def initiate_file_processing(file, db_name, collection_name, connString):
    anvil.server.launch_background_task('store_data', file, db_name, collection_name, connString)
    return "Processing started"
  


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
