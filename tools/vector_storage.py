import json
from mappers.profile_mapper import get_profile_documents

profile_data_file_path="../data/client_profiles.json"
products_data_file_path="../data/product_catalog.json"


def get_client_profiles_documents():
    """Get the client profile documents"""
    try:
        with open(profile_data_file_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        return get_profile_documents(profiles, products_data_file_path)
    except FileNotFoundError:
        print(f"Error: File not found in {profile_data_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {profile_data_file_path}")
        return []


# def get_product_catalog_documents():
#     """Get the product catalog documents"""
#     try:
#
#     except FileNotFoundError:
#         print(f"Error: File not found in {products_data_file_path}")


print(get_client_profiles_documents())