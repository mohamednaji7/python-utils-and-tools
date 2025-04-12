import os
import json
from openai import AzureOpenAI
import tiktoken

from utils import TimeEstimator, FileSystemProcessor as fsp

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Fetch variables
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("OPENAI_API_VERSION")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not (api_key and api_version and endpoint):
    raise ValueError("ENV are not set")

# Initialize the OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
    )




# # Open the JSON file
# with open('input/results_deduplicated.json', 'r') as file:
#     # Load the JSON data
#     files = json.load(file)

# Now you can work with the data

# print(type(files), len(files))
# print(files[0].keys())

    

def tokens_size(model, text):

    # Use tiktoken for more accurate token counting
    encoding = tiktoken.encoding_for_model(model)
    
    # Tokenize the text
    tokens = encoding.encode(text)

    
    return len(tokens)



def chunk_text(model, text, max_tokens=500, overlap=50):
    """
    Chunk long text into smaller, overlapping pieces.
    
    :param text: Input text to chunk
    :param max_tokens: Maximum number of tokens per chunk
    :param overlap: Number of tokens to overlap between chunks
    :return: List of text chunks
    """
    # Use tiktoken for more accurate token counting
    encoding = tiktoken.encoding_for_model(model)
    
    # Tokenize the text
    tokens = encoding.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        # Extract a chunk of tokens
        chunk_tokens = tokens[i:i + max_tokens]
        
        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

def make_metdata(input_path, output_path, model, max_tokens=500, overlap=50):
    print("Processing files...")

    files = fsp.load_json(input_path)
    records_id_metadata = []


    for idx, file in enumerate(files):
        
        # file_path = file['path']
        with open(file['path'], 'r') as f:
            text = f.read()
        
        # Chunk the text
        chunks = chunk_text(model, text, max_tokens, overlap)

        for chunk_idx, chunk in enumerate(chunks):
            # Metadata to store with the vector
            metadata = {
                'original_doc_index': idx,
                'chunk_idx': chunk_idx,
                'chunk_content': chunk,
                'number_of_chunks': len(chunks),
            }

            for key, value in file['metadata'].items():
                metadata[key] = value
            
            records_id_metadata.append(
                {
                    "record_id": file['id'],
                    "metadata": metadata,
                }
            )
            
    fsp.save_json(output_path, records_id_metadata, indent=2, append_not_overwrite=False, backup=True, ensure_ascii=False)






def get_embeddings(txt, model):
  embedding = client.embeddings.create(
    model=model,
    input=txt,
    encoding_format="float" 
  )
  return embedding.data[0].embedding

# embedding = get_embeddings("Attenion is all you need", MODEL)

# print("embedding")
# print(type(embedding))
# print(len(embedding))



def add_embedding(records_id_metadata_path, records_path, model):
    print("Making embeddings files...")

    records = []

    records_id_metadata = fsp.load_json(records_id_metadata_path)

    print(f"Total records id metadata: {len(records_id_metadata)}")
    estimator = TimeEstimator(len(records_id_metadata))


    for record_id_metadata in records_id_metadata: 
        # chunk and embed the text  
        estimator.start_iteration()

        # Embed the chunk
        embedding = get_embeddings(
            record_id_metadata['metadata']['chunk_content'],
            model
            )

        records.append((
            record_id_metadata['record_id'],
            embedding,
            record_id_metadata['metadata']
        ))

        estimator.update_processing_time()

    # print(new_records[0])
    # fsp.restore_backup_file(records_path)
    fsp.save_json(records_path, records, indent=2, backup=True, append_not_overwrite=False)

