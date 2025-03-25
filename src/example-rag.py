

from rag import (
    process_chunk_and_embed,
    supabase_upload_records
)

# # Process the files
# process_chunk_and_embed(
#     'rag_data/input/results_deduplicated.json',
#     'rag_data/output/records.json'      
#     )

supabase_upload_records(
    'rag_data/output/records.json',
    "new-websites-data")