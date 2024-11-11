from fastapi import FastAPI, HTTPException, Header, Depends
import logging
from datetime import datetime
import uuid
from typing import List, Optional, Dict

# Import the models
from models.models import (
    AuthRequest,
    AuthResponse,
    EmbeddingRequest,
    ImageURLsRequest,
    GenerateAndPostEmbeddingRequest,
    GetUUIDsRequest,
    SearchEmbeddingRequest
)

# Import services
from services.authentication import authenticate_user, validate_token
from services.embedding import generate_embedding, parse_algorithm
from services.qdrant import upsert_embedding, get_all_uuids,search_embedding

# Setup logging configuration (datewise logging)
log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Initialize FastAPI application
app = FastAPI()

# API Endpoints
@app.post("/Authenticate", response_model=AuthResponse)
async def authenticate(request: AuthRequest):
    try:
        long_term_token, expiry = authenticate_user(request.username, request.OTP_Token, request.long_term_days)
        logging.info(f"User '{request.username}' authenticated successfully. Token issued for {request.long_term_days} days.")
        return AuthResponse(long_term_token=long_term_token, expiry=expiry)
    except HTTPException as e:
        logging.error(f"Authentication error: {str(e)}")
        raise e

async def validate_long_term_token(x_long_term_token: Optional[str] = Header(None)):
    return validate_token(x_long_term_token)

@app.post("/GetEmbeddingsByImageURL")
async def get_embedding_by_image_url(request: ImageURLsRequest, token_data: dict = Depends(validate_long_term_token)):
    try:
        embeddings = []
        for url in request.image_urls:
            embedding = generate_embedding(request.algorithm, url)
            embeddings.append({
                "image_url": url,
                "embedding": embedding
            })
            #embeddings.append(embedding)
        logging.info(f"Retrieved embeddings for {len(request.image_urls)} images.")
        return {"status": "success", "result": embeddings}
    except Exception as e:
        logging.error(f"Error in get_embedding_by_image_url: ", e )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/PostEmbedding")
async def post_embedding(request: EmbeddingRequest, token_data: dict = Depends(validate_long_term_token)):
    try:
        algorithm_name, vector_size = parse_algorithm(request.algorithm)
        responses = []
        for record in request.embeddings:
            uuid_str = record.uuid
            vector = record.vector
            metadata = record.metadata
            print(f"-----------{algorithm_name}_{vector_size}-----------------")
            upsert_embedding(algorithm_name,vector_size, uuid_str, vector, metadata)
            responses.append({"uuid": uuid_str, "status": "success"})

        logging.info(f"Posted {len(request.embeddings)} embeddings successfully.")
        return {"status": "success", "message": "Embeddings posted successfully", "result": responses}
    except Exception as e:
        logging.error(f"Error in post_embedding: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/GenerateAndPostEmbeddingByImageURL")
async def generate_and_post_embedding_by_image_url(request: GenerateAndPostEmbeddingRequest, token_data: dict = Depends(validate_long_term_token)):
    try:
        algorithm_name, vector_size = parse_algorithm(request.algorithm)

        responses = []
        for url,uuid_str in zip(request.image_urls,request.uuids):
            embedding = generate_embedding(request.algorithm, url)
            upsert_embedding(algorithm_name, vector_size,  uuid_str, embedding, request.metadata)
            responses.append({"uuid": uuid_str, "image_url": url, "status": "success"})

        logging.info(f"Generated and posted embeddings for {len(request.image_urls)} images using {algorithm_name} with vector size {vector_size}.")
        return {"status": "success", "message": "Embeddings generated and posted successfully",  "result": responses }
    except Exception as e:
        logging.error(f"Error in generate_and_post_embedding_by_image_url: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/GetUUIDs")
async def get_uuids(request: GetUUIDsRequest,  token_data: dict = Depends(validate_long_term_token)):
    try:
        algorithm_name, vector_size = parse_algorithm(request.algorithm)

        responses = []
        responses = get_all_uuids(algorithm_name, request.uuids)
        return  {"status": "success", "result": responses, "algo":algorithm_name }
        logging.info(f"Get UUIDs.")
    except Exception as e:
        logging.error(f"Error in calling GetUUIDs: {str(e)}")
        return {"status": "error", "message": str(e)}      


@app.post("/SearchByEmbedding")
async def search_embedding_endpoint(request: SearchEmbeddingRequest, token_data: dict = Depends(validate_long_term_token)):
    """
    Search for similar embeddings based on the provided query vector.
    """
    try:
        algorithm_name, vector_size = parse_algorithm(request.algorithm)
        results = search_embedding(algorithm_name, request.query_vector, request.top_k)
        logging.info(f"Performed search on collection '{request.algorithm}' with top_k={request.top_k}.")
        return {"status": "success", "results": results}
    except Exception as e:
        logging.error(f"Error in search_embedding_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
