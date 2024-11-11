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
    "username": "test_user",
    "OTP_Token": "123456",
    "long_term_days": 30
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
- **Endpoint**: `/GetEmbeddingByImagingURL`
- **Method**: `POST`
- **Description**: Retrieves embeddings for the provided image URLs.
- **Body**:
  ```json
  {
    "image_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ],
    "algorithm": "miewid_2048"
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
- **Description**: Stores the given embeddings in the Qdrant database.
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
    "algorithm": "example_1024"
  }
  ```

### 4. Batch Post Embedding
- **Endpoint**: `/BatchPostEmbedding`
- **Method**: `POST`
- **Description**: Inserts a batch of embeddings into the Qdrant database.
- **Body**:
  ```json
  {
    "embeddings": [
      {
        "uuid": "uuid_1",
        "vector": [0.1, 0.2, 0.3],
        "metadata": {
          "source": "web",
          "category": "nature"
        }
      },
      {
        "uuid": "uuid_2",
        "vector": [0.4, 0.5, 0.6],
        "metadata": {
          "source": "mobile",
          "category": "urban"
        }
      }
    ],
    "algorithm": "example_1024"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Embeddings posted successfully",
    "result": [
      {
        "uuid": "uuid_1",
        "status": "success"
      },
      {
        "uuid": "uuid_2",
        "status": "success"
      }
    ]
  }
  ```

### 5. Search Embedding
- **Endpoint**: `/SearchByEmbedding`
- **Method**: `POST`
- **Description**: Searches the Qdrant database for similar embeddings to the given query vector.
- **Body**:
  ```json
  {
    "collection_name": "example_1024",
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

### 6. Get UUIDs
- **Endpoint**: `/GetUUIDs`
- **Method**: `GET`
- **Description**: Retrieves all UUIDs from the specified Qdrant collection.
- **Parameters**: `collection_name` (query parameter)
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

## Running Tests
The repository includes unit tests that can be run to validate functionality. To execute the tests:

```sh
pytest
```


