import importlib
from fastapi import HTTPException

def parse_algorithm(algorithm: str):
    try:
        algorithm_name, vector_size = algorithm.split('_')
        vector_size = int(vector_size)
        return f"{algorithm_name.lower()}_{str(vector_size)}", vector_size
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid algorithm format. Expected format: {algorithm_name}_{vector_size}")

def get_embedding_class(algorithm_name: str):
    try:
        module = importlib.import_module(f"algos.{algorithm_name}")
        embedding_class = getattr(module, algorithm_name.lower())
        return embedding_class
    except ModuleNotFoundError:
        raise HTTPException(status_code=400, detail=f"Algorithm '{algorithm_name}' not found")
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Class '{algorithm_name.capitalize()}' not found in module '{algorithm_name}'")

def generate_embedding(algorithm: str, image_url: str):
    algorithm_name, _ = parse_algorithm(algorithm)
    embedding_class = get_embedding_class(algorithm_name)
    #model, device = embedding_class.load_model("")
    return embedding_class.extract_embeddings_from_path(embedding_class, one_image=image_url)
