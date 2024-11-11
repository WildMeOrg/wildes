import qdrant_client
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType, Filter, SearchParams
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read Qdrant configuration from .env file
QDRANT_HOST = os.getenv("QDRANT_HOST", "127.0.0.1")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

# Initialize Qdrant client using environment variables
qdrant_client = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def ensure_collection_exists(collection_name: str, vector_size: int):
    """
    Ensure that the specified collection exists in Qdrant. If it does not exist, create it.
    
    :param collection_name: Name of the Qdrant collection
    :param vector_size: Size of the embedding vector
    """
    collections = qdrant_client.get_collections().collections
    if not any(collection.name == collection_name for collection in collections):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
#            payload_schema={
#                "uuid": PayloadSchemaType.keyword,
#                "metadata": PayloadSchemaType.object
#            }
        )
        print(f"Collection '{collection_name}' created with vector size {vector_size}.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def upsert_embedding(collection_name: str, v_size: int,  uuid: str, vector: list, metadata: dict = None):
    """
    Upsert an embedding into the Qdrant collection.

    :param collection_name: Name of the Qdrant collection
    :param uuid: Unique identifier for the embedding
    :param vector: The embedding vector
    :param metadata: Optional metadata dictionary
    """
    # Ensure that the collection exists before trying to upsert data
    vector_size = v_size
    ensure_collection_exists(collection_name, vector_size)

    # Upsert the embedding data
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[{
            'id': uuid,
            'vector': vector,
            'payload': {
                "uuid": uuid,
                "metadata": metadata
            } if metadata else {"uuid": uuid}
        }]
    )


def get_all_uuids(collection_name: str, uuid_list: list = None):
    """
    Retrieve all UUIDs from the specified Qdrant collection.
    If a list of UUIDs is provided, it will search for those UUIDs in the collection and return the existing ones.

    :param collection_name: Name of the Qdrant collection
    :param uuid_list: Optional list of UUIDs to search in the collection
    :return: A list of UUIDs found in the collection
    """
    try:
        if uuid_list is None:
            # Perform a scroll search to fetch all items in the collection if no UUID list is provided
            all_uuids = []
            has_more = True
            next_offset = None

            while has_more:
                response, next_offset = qdrant_client.scroll(
                    collection_name=collection_name,
                    offset=next_offset,
                    limit=100  # Adjust the limit as needed
                )
                
                # Append the UUIDs from the current response to the list
                all_uuids.extend([point.id for point in response])

                # If there's no more data to scroll, exit the loop
                has_more = next_offset is not None

            return all_uuids
        else:
            # Search for the specified UUIDs in the collection
            existing_uuids = []
            for uuid in uuid_list:
                try:
                    response = qdrant_client.retrieve(
                        collection_name=collection_name,
                        ids=[uuid]
                    )
                    if response:
                        existing_uuids.append(uuid)
                except Exception as e:
                    print(f"Error while retrieving UUID {uuid}: {e}")
                    continue

            return existing_uuids

    except Exception as e:
        print(f"Error while retrieving UUIDs: {e}")
        return []



def search_embedding(collection_name: str, query_vector: list, top_k: int = 5):
    """
    Search for the closest embeddings in the specified Qdrant collection.

    :param collection_name: Name of the Qdrant collection
    :param query_vector: The query embedding vector
    :param top_k: The number of nearest neighbors to return
    :return: A list of the closest embeddings
    """
    try:
        # Perform the search
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k #,
            #search_params=SearchParams(distance=Distance.COSINE)
        )
 
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })

        return results
    except Exception as e:
        print(f"Error while searching embeddings: {e}")
        return []
