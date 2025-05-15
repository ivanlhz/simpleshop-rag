import json

from mappers.product_catalog_mapper import get_products_documents
from mappers.profile_mapper import get_profile_documents

profile_data_file_path="../data/client_profiles.json"
products_data_file_path="../data/product_catalog.json"


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



print(get_product_catalog_documents())