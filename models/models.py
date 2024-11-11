from pydantic import BaseModel
from typing import List, Optional, Dict

class AuthRequest(BaseModel):
    username: str
    OTP_Token: str
    long_term_days: int

class AuthResponse(BaseModel):
    long_term_token: str
    expiry: str

class Embedding(BaseModel):
    uuid: str
    vector: List[float]  # Numeric array of floats
    metadata: Optional[Dict[str, str]] = None  # Optional metadata key-value pairs

class EmbeddingRequest(BaseModel):
    embeddings: List[Embedding]
    algorithm: str

class ImageURLsRequest(BaseModel):
    image_urls: List[str]
    algorithm: str
    metadata: Optional[Dict[str, str]] = None
    limit: Optional[int] = 10

class GenerateAndPostEmbeddingRequest(BaseModel):
    image_urls: List[str]
    uuids : List[str]
    algorithm: str
    metadata: Optional[Dict[str, str]] = None

class GetUUIDsRequest(BaseModel):
    uuids:Optional[List[str]] = None
    algorithm: str

class SearchEmbeddingRequest(BaseModel):
    algorithm: str
    query_vector: List[float]  # The embedding vector to use as the query
    top_k: Optional[int] = 5  # Optional, defaults to 5; number of nearest neighbors to return
