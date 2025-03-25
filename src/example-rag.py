

from rag import (
    make_metdata,
    add_embedding,
    supabase_upload_records
)

make_metdata(
    'rag_data/input/results_deduplicated.json',
    'rag_data/output/records_id_metadata.json'      
)


add_embedding(
    'rag_data/output/records_id_metadata.json' ,
    'rag_data/output/records.json'      
    )

supabase_upload_records(
    'rag_data/output/records.json',
    "new-websites-data")