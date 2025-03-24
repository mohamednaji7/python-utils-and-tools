# https://colab.research.google.com/drive/11JC0iHtyr1Fpy4aoYI_qsn5BTGdb-Zk7
# https://colab.research.google.com/drive/1V-yQhWnEvWh7WSoxvpVAdxW5fEQ0-PmB

import os
import json
from openai import AzureOpenAI
import vecs
import tiktoken

from utils import init_logger, TimeEstimator
init_logger()

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Fetch variables
api_key = os.getenv("AZURE_OPENAI_KEY")
MODEL = os.getenv("AZURE_OPENAI_MODELID")
api_version = os.getenv("OPENAI_API_VERSION")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not (api_key and MODEL and api_version and endpoint):
    raise ValueError("ENV are not set")

# Initialize the OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
    )



# Fetch variables
user = os.getenv("user")
host = os.getenv("host")
port = os.getenv("port")
dbname = os.getenv("dbname")
password = os.getenv("password")


# DB_CONNECTION 
DB_CONNECTION = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"




vx = vecs.create_client(DB_CONNECTION)
dimension = 1536
docs = vx.get_or_create_collection(name="new-websites-data", dimension=dimension)

docs.create_index(measure=vecs.IndexMeasure.cosine_distance)




# Open the JSON file
with open('results_deduplicated.json', 'r') as file:
    # Load the JSON data
    files = json.load(file)

# Now you can work with the data

# print(type(files), len(files))
# print(files[0].keys())

def get_embeddings(txt, model):
  embedding = client.embeddings.create(
    model=model,
    input=txt,
    encoding_format="float" 
  )
  return embedding.data[0].embedding

embedding = get_embeddings("Attenion is all you need", MODEL)

# print("embedding")
# print(type(embedding))
# print(len(embedding))

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

def tokens_size(model, text):

    # Use tiktoken for more accurate token counting
    encoding = tiktoken.encoding_for_model(model)
    
    # Tokenize the text
    tokens = encoding.encode(text)

    
    return len(tokens)




def chunk_and_embed(files):
    records = []
    record_id = 0

    # Example usage:
    estimator = TimeEstimator(len(files))



    for idx, file in enumerate(files):
        
        # chunk and embed the text  
        estimator.start_iteration()

        text = file['main_content']

        # Chunk the text
        chunks = chunk_text(MODEL, text)



        for chunk_idx, chunk in enumerate(chunks):
            # Embed the chunk
            embedding = get_embeddings(chunk, MODEL)

            # Metadata to store with the vector
            metadata = {
                'title': file['title'],
                'description': file['description'],
                'scrape_timestamp': file['scrape_timestamp'],
                'url': file['url'],
                'domain': file['domain'],
                'category': file['cat'],
                'subdir': file['subdir'],
                'original_doc_index': idx,
                'chunks_length': len(chunks),
                'doc_tokens_size': tokens_size(MODEL, text),
                'chunk_idx': chunk_idx,
                'doc_idx': idx
            }
            
            records.append((
                record_id,
                embedding,
                metadata
            ))
            
            # break
        record_id += 1
        estimator.update_processing_time()
        # break
    return records 

records = chunk_and_embed(files)
# print(records)
docs.upsert(records)