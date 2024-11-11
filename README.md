# Wildes - Wildme embedding service

This project provides a set of microservices to interact with a Qdrant vector database. These services allow users to generate embeddings using a variety of algorithms, store them in Qdrant, and perform various operations such as retrieving, searching, and upserting embedding vectors.

## Features
- **Generate Embeddings from Image URLs**: Generate embeddings from provided image URLs using a specified algorithm.
- **Store Embeddings in Qdrant**: Upsert generated embeddings into the Qdrant vector database.
- **Search for Similar Embeddings**: Perform a search in Qdrant to find embeddings similar to a given query vector.
- **UUID Management**: Retrieve or validate UUIDs from the Qdrant database.

## Technologies Used
- **Python**: The microservices are built using Python.
- **FastAPI**: Provides the RESTful API services.
- **Qdrant**: Vector database for efficient vector search.
- **Docker**: Containerization for scalability and easy deployment.
- **Pydantic**: Data validation and serialization.

## Installation

### Prerequisites
- **Docker**: Ensure Docker is installed to run the services in a container.
- **Python 3.7+**: Required for running the API locally (if not using Docker).

### Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/wildme/wildes.git
   cd wildes
   ```

2. **Install Dependencies**
   If you are running the application locally:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run with Docker**
   To run the services using Docker:
   ```sh
   docker build -t qdrant-api .
   docker run -p 8000:8000 qdrant-api
   ```

4. **Environment Configuration**
   Create a `.env` file for environment configuration. An example of the `.env` file:
   ```env
   QDRANT_HOST=127.0.0.1
   QDRANT_PORT=6333
   API_KEY=your_api_key_here
   ```

## API Endpoints

### 1. Authenticate
- **Endpoint**: `/Authenticate`
- **Method**: `POST`
- **Description**: Authenticates a user and returns a long-term token.
- **Body**:
  ```json
   {
     "username": "wildme_ess",
     "OTP_Token": "XXXXXX",
     "long_term_days": 300
   }
  ```
- **Response**:
  ```json
  {
    "long_term_token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
    "expiry": "25-10-2024 10:00:00"
  }
  ```

### 2. Get Embedding by Image URLs
- **Endpoint**: `/GetEmbeddingByImageURL`
- **Method**: `POST`
- **Description**: Retrieves embeddings for the provided image URLs (But does not Read/Write from Qdrant ).
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````
- **Body**:
  ```json
  {
    "image_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ],
    "algorithm": "miewid_2152"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "embeddings": [
      {
        "image_url": "https://example.com/image1.jpg",
        "embedding": [0.1, 0.2, 0.3]
      },
      {
        "image_url": "https://example.com/image2.jpg",
        "embedding": [0.4, 0.5, 0.6]
      }
    ]
  }
  ```

### 3. Post Embedding
- **Endpoint**: `/PostEmbedding`
- **Method**: `POST`
- **Description**: Stores the given embeddings and uuid in the Qdrant database.
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````
- **Body**:
  ```json
  {
    "embeddings": [
      {
        "uuid": "a7b3c2d8-90f0-4d1a-a62c-bb72f3ac5041",
        "vector": [0.1, 0.2, 0.3],
        "metadata": {
          "source": "web",
          "category": "nature"
        }
      }
    ],
    "algorithm": "miewid_2152"
  }
  ```

### 4. GenerateAndPostEmbeddingByImageURL Embedding
- **Endpoint**: `/GenerateAndPostEmbeddingByImageURL`
- **Method**: `POST`
- **Description**: For the given the list of image_urls, generate embeddings, store the given embeddings in the Qdrant database.
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````  
- **Body**:
  ```json
    {
       "image_urls": ["/data/db/wess/chim_image.jpg", "/data/db/wess/chim_image.jpg" ], 
       "uuids":["570c774b-935a-4f67-83f2-57c214a341e7","c2779b76-8418-4d91-bb42-cf47fb5bb6db"],
       "algorithm": "miewid_2152"
   }
  ```
- **Response**:
  ```json
   {
     "status": "success",
     "message": "Embeddings generated and posted successfully",
     "result": [
       {
         "uuid": "570c774b-935a-4f67-83f2-57c214a341e7",
         "image_url": "/data/db/wess/chim_image.jpg",
         "status": "success"
       },
       {
         "uuid": "c2779b76-8418-4d91-bb42-cf47fb5bb6db",
         "image_url": "/data/db/wess/chim_image.jpg",
         "status": "success"
       }
     ]
   }
  ```
  
### 5. Search By Embedding
- **Endpoint**: `/SearchByEmbedding`
- **Method**: `POST`
- **Description**: Searches the Qdrant database for similar embeddings to the given query vector.
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````
- **Body**:
  ```json
  {
    "algorithm": "miewid_2152",
    "query_vector": [0.1, 0.2, 0.3, 0.4, 0.5],
    "top_k": 5
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "results": [
      {
        "id": "a7b3c2d8-90f0-4d1a-a62c-bb72f3ac5041",
        "score": 0.95,
        "payload": {
          "uuid": "a7b3c2d8-90f0-4d1a-a62c-bb72f3ac5041",
          "metadata": {
            "source": "web",
            "category": "nature"
          }
        }
      }
    ]
  }
  ```

### 6. Get UUIDs All
- **Endpoint**: `/GetUUIDs`
- **Method**: `POST`
- **Description**: Retrieves all UUIDs from the specified Qdrant collection.
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````
- **Body**:
  ```json
    {
         "algorithm": "miewid_2152"
    }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "uuids": [
      "uuid_1",
      "uuid_2",
      "uuid_3"
    ]
  }
  ```


### 7. Get UUIDs
- **Endpoint**: `/GetUUIDs`
- **Method**: `POST`
- **Description**: Retrieves UUIDs for the given list of UUIDs the specified Qdrant collection.
- **Headers**:
  ```json
     {
     "x-long-term-token": "e8d6f184-c839-4822-bae4-4542fa50a1d4",
     "Content-Type": "application/json"
     }
  ````
- **Body**:
  ```json
   {
       "uuids":["a7b3c2d8-90f0-4d1a-a62c-bb72f3ac5041","c2779b76-8418-4d91-bb42-cf47fb5bb6da"],
       "algorithm": "miewid_2152"
   }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "uuids": [
     "a7b3c2d8-90f0-4d1a-a62c-bb72f3ac5041",
     "c2779b76-8418-4d91-bb42-cf47fb5bb6da"
    ]
  }
  ```

## Running The services
To run the service

```sh
nohup python3.10 -m uvicorn main:app --host 0.0.0.0 --port 6444 --reload &
```


