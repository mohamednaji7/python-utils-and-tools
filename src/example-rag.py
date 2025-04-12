import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


from pyut.rag.embed import (
    make_metdata,
    add_embedding
)

from pyut.rag.upload_records import supabase_upload_records



model = 'text-embedding-3-small'
dimension = 1536

make_metdata(
    'data/King Kong - Quantum  Growth.json',
    'data/records_id_metadata.json',
    model
)


add_embedding(
    'data/records_id_metadata.json' ,
    'data/records.json' ,
    model  
    )

supabase_upload_records(
    'data/records.json' ,
    "king_kong_quantum_growth",
    dimension
    )