# data preparation
import pandas as pd
import os
import json

# flatten the json data
def load_and_flatten_data(json_file_path):
    """Loads data from JSON and flattens it into a list of API documents."""
    flattened_apis = []
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        return []

    doc_id_counter = 0
    for module_name, module_data in data.items():
        for class_name, class_details in module_data.get("subsections", {}).items():
            api_full_name = f"{module_name}.{class_name}"

            # Construct text for embedding
            # Consider adding a brief scraped description here if possible in the future
            text_for_embedding = f"API Name: {class_name}. Belongs to module: {module_name}. "
            text_for_embedding += f"Signature: {class_details.get('class_signature', '')}. "
            # Example code can be long; consider truncating or summarizing for embedding if performance issues arise
            text_for_embedding += f"Example Usage: {class_details.get('example_code', '')}"

            api_doc = {
                "id": str(doc_id_counter), # ChromaDB requires string IDs
                "api_full_name": api_full_name,
                "module_name": module_name,
                "class_name": class_name,
                "link": class_details.get("link", ""),
                "class_signature": class_details.get("class_signature", ""),
                "example_code": class_details.get("example_code", ""),
                "text_for_embedding": text_for_embedding
            }
            flattened_apis.append(api_doc)
            doc_id_counter += 1
    return flattened_apis