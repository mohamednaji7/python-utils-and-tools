import json 
from utils import TimeEstimator, FileSystemProcessor as fsp

import os
import vecs


from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


# Fetch variables
user = os.getenv("user")
host = os.getenv("host")
port = os.getenv("port")
dbname = os.getenv("dbname")
password = os.getenv("password")


# DB_CONNECTION 
DB_CONNECTION = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

vx = vecs.create_client(DB_CONNECTION)


def supabase_upload_records(records_path, doc_name, dimension):
    docs = vx.get_or_create_collection(name=doc_name, dimension=dimension)

    docs.create_index(measure=vecs.IndexMeasure.cosine_distance)

    records = fsp.load_json(records_path)
    

    # BATCH_SIZE = 2
    BATCH_SIZE = 128
    clock = TimeEstimator(len(records)//BATCH_SIZE)
    for i in range(0, len(records), BATCH_SIZE):
        clock.start_iteration()
        batch = records[i:i+BATCH_SIZE]
        docs.upsert(batch)
        clock.update_processing_time()
        # break

