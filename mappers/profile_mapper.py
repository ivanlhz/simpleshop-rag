from langchain_core.documents import Document

def get_profile_measurements(body_measurements):
    measurements = ", ".join([f"{k.replace('_cm', '')}: {v}cm" for k, v in body_measurements.items()])
    if not measurements:
        measurements: 'Not available'

    return measurements

def get_purchases_history(purchases_history):
    purchase_history_str_list = []
    for item in purchases_history:
        purchase_history_str_list.append(
            f"Product: {item.get('product_id', 'N/A')}, Size: {item.get('size_purchased', 'N/A')}, Fit feedback: {item.get('fit_feedback', 'No feedback')}."
        )

    purchases_history_str = " ".join(
        purchase_history_str_list) if purchase_history_str_list else "No purchase history."

    return purchases_history_str

def get_profile_documents(profiles, profile_data_file_path):
    documents = []
    for profile in profiles:
        body_measurements = profile.get('body_measurements', {})
        measurements = get_profile_measurements(body_measurements)
        purchases_history = get_purchases_history(profile.get('purchase_history', []))

        page_content = (
            f"Profile: {profile.get('name', profile['client_id'])}. "
            f"ID: {profile['client_id']}. "
            f"Age: {profile.get('age', 'N/A')} years old. "
            f"Height: {profile.get('height_cm', 'N/A')}cm. "
            f"Weight: {profile.get('weight_kg', 'N/A')}kg. "
            f"Body measurements: {measurements}. "
            f"Preferred fit: {profile.get('preferred_fit', 'No preferred fit')}. "
            f"Purchase history: {purchases_history}"
        )

        # La metadata contiene campos estructurados.
        metadata = {
            "source": profile_data_file_path,
            "entity_id": profile["client_id"],
            "entity_type": "profile",
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    return documents