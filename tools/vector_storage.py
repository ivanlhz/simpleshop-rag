import json
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from mappers.product_catalog_mapper import get_products_documents
from mappers.profile_mapper import get_profile_documents
from langchain_community.vectorstores import FAISS

# Cargar rutas desde variables de entorno, con valores por defecto si no existen
profile_data_file_path = os.getenv("PROFILE_DATA_FILE_PATH", "./data/client_profiles.json")
products_data_file_path = os.getenv("PRODUCTS_DATA_FILE_PATH", "./data/product_catalog.json")
VECTOR_STORE_FAISS_NAME = os.getenv("VECTOR_STORE_FAISS_NAME", "./data/db")

load_dotenv()

def get_client_profiles_documents():
    """Get the client profile documents"""
    try:
        with open(profile_data_file_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        return get_profile_documents(profiles, profile_data_file_path)
    except FileNotFoundError:
        print(f"Error: File not found in {profile_data_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {profile_data_file_path}")
        return []


def get_product_catalog_documents():
    """Get the product catalog documents"""
    try:
        with open(products_data_file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        return get_products_documents(products, products_data_file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {products_data_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {products_data_file_path}")
        return []
    except KeyError as e:
        print(f"Error: Missing key '{e}' in one of the product objects in {products_data_file_path}")
        return []



def get_vector_storage():
    """Create the vector storage"""
    profile_documents = get_client_profiles_documents()
    product_documents = get_product_catalog_documents()
    all_documents = profile_documents + product_documents

    embeddings_model = OpenAIEmbeddings()

    vector_store: FAISS

    if os.path.exists(VECTOR_STORE_FAISS_NAME):
        print(f"Loading existing Vector Store from '{VECTOR_STORE_FAISS_NAME}'...")
        try:
            vector_store = FAISS.load_local(VECTOR_STORE_FAISS_NAME, embeddings_model,
                             allow_dangerous_deserialization=True)
            print("Vector Store loaded.")
        except Exception as e:
            print(f"Could not load existing Vector Store: {e}. A new one will be created.")
            vector_store = None
    else :
        vector_store = FAISS.from_documents(all_documents, embeddings_model)
        vector_store.save_local(VECTOR_STORE_FAISS_NAME)

    return vector_store

def get_user_profile_info(name: str):
    """Get user profile info from the vector store"""
    vector_storage = get_vector_storage()
    retriever = vector_storage.as_retriever(search_kwargs={'k': 3, 'filter': {'entity_type': 'profile'}})
    result = retriever.invoke(f"profile information for user {name}")
    return result

def search_product(query: str):
    """Get information about product from vector store"""
    vector_storage = get_vector_storage()
    retriever = vector_storage.as_retriever(search_kwargs={'k': 3, 'filter': {'entity_type': 'product'}})
    docs = retriever.invoke(f"{query}")
    
    if not docs or len(docs) == 0:
        return f"No se encontró información para la consulta: {query}. Por favor intenta con otra búsqueda."
    
    product_info = []
    for doc in docs:
        product_info.append(doc.page_content)
    
    return "\n\n".join(product_info)
