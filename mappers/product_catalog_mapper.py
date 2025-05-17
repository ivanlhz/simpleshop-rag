from langchain_core.documents import Document

def get_size_chart_description(size_charts):
    size_chart_str_parts = []
    for size, measurements in size_charts:
        m_parts = []
        if "bust_cm" in measurements:
            m_parts.append(f"bust {measurements['bust_cm']}cm")
        if "waist_cm" in measurements:
            m_parts.append(f"waist {measurements['waist_cm']}cm")
        if "hips_cm" in measurements:
            m_parts.append(f"hips {measurements['hips_cm']}cm")
        size_measurements_str = ", ".join(m_parts)
        size_chart_str_parts.append(f"Size {size}: {size_measurements_str}")
    size_chart_description = ". ".join(size_chart_str_parts)
    if not size_chart_description:
        size_chart_description = "Size chart not specified."
    return size_chart_description


def get_products_documents(products, products_data_file_path):
    documents = []
    for product in products:
        available_sizes_str = ", ".join(product.get("available_sizes", ["N/A"]))
        size_chart_description = get_size_chart_description(product.get("size_chart", {}).items())

        model_ref_str = "Model reference not specified."
        model_ref = product.get("model_reference", {})
        if model_ref.get("height_cm") and model_ref.get("wearing_size"):
            model_ref_str = f"Model is {model_ref['height_cm']}cm tall and wears size {model_ref['wearing_size']}."

        page_content = (
            f"Product: {product.get('name', product.get('product_id', 'Unknown'))}. "
            f"ID: {product.get('product_id', 'Unknown')}. "
            f"Description: {product.get('description', 'No description available.')} "
            f"Available sizes: {available_sizes_str}. "
            f"Fit: {product.get('fit', 'N/A')}. Fabric: {product.get('fabric', 'N/A')}. "
            f"{model_ref_str} "
            f"Size details: {size_chart_description}"
        )

        metadata = {
            "source": products_data_file_path,
            "entity_id": product.get("product_id", f"product_autogen_{len(documents)}"),
            "entity_type": "product",
            **product
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    return documents