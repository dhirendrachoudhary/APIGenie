# create and inti to vectorize the data
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

def initialize_embedding_model(model_name):
    """Initializes and returns the Sentence Transformer model."""
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Embedding model loaded.")
    return model

def create_and_populate_vector_db(apis, model, db_path, collection_name):
    """Creates embeddings and populates ChromaDB."""
    if not apis:
        print("No APIs to process for vector DB.")
        return None

    print("Initializing ChromaDB client...")
    client = chromadb.PersistentClient(path=db_path)

    # Get or create collection
    try:
        collection = client.get_collection(name=collection_name)
        print(f"Using existing collection: {collection_name}")
        # Optional: Clear collection if you want to re-ingest every time
        # client.delete_collection(name=collection_name)
        # collection = client.create_collection(name=collection_name)
        # print(f"Re-created collection: {collection_name}")
    except: # Simple catch-all for this example, refine for production
        print(f"Creating new collection: {collection_name}")
        collection = client.create_collection(name=collection_name)

    print(f"Generating embeddings for {len(apis)} API documents...")
    texts_to_embed = [doc['text_for_embedding'] for doc in apis]
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)

    # Prepare data for ChromaDB
    documents_for_chroma = [doc['text_for_embedding'] for doc in apis] # What text Chroma stores
    metadatas_for_chroma = [
        {
            "api_full_name": doc["api_full_name"],
            "module_name": doc["module_name"],
            "class_name": doc["class_name"],
            "link": doc["link"],
            "signature": doc["class_signature"]
            # Exclude full example_code and text_for_embedding from metadata to keep it lean
            # We already have the ID to fetch the full original doc if needed
        } for doc in apis
    ]
    ids_for_chroma = [doc['id'] for doc in apis]

    # Check if documents already exist to avoid duplicates or decide on update strategy
    # For simplicity here, we'll assume we add if not exists, or re-add if collection was cleared.
    # A more robust way is to check existing IDs.
    existing_docs = collection.get(ids=ids_for_chroma)
    new_ids_for_chroma = []
    new_embeddings = []
    new_documents_for_chroma = []
    new_metadatas_for_chroma = []

    for i, doc_id in enumerate(ids_for_chroma):
        if doc_id not in existing_docs['ids']:
            new_ids_for_chroma.append(doc_id)
            new_embeddings.append(embeddings[i])
            new_documents_for_chroma.append(documents_for_chroma[i])
            new_metadatas_for_chroma.append(metadatas_for_chroma[i])

    if new_ids_for_chroma:
        print(f"Adding {len(new_ids_for_chroma)} new documents to ChromaDB...")
        collection.add(
            embeddings=np.array(new_embeddings).tolist(), # Ensure it's a list of lists/np.array
            documents=new_documents_for_chroma,
            metadatas=new_metadatas_for_chroma,
            ids=new_ids_for_chroma
        )
        print(f"{len(new_ids_for_chroma)} documents added/updated in collection '{collection_name}'.")
    else:
        print("No new documents to add. All documents might already exist.")

    return collection

# retrieve relevant APIs
def retrieve_relevant_apis(query_text, model, collection, n_results=5):
    """Embeds the query and retrieves relevant APIs from ChromaDB."""
    print(f"\nUser Query: '{query_text}'")
    query_embedding = model.encode([query_text])[0] # Get the first (and only) embedding

    results = collection.query(
        query_embeddings=[query_embedding.tolist()], # Chroma expects a list of embeddings
        n_results=n_results,
        include=['metadatas', 'documents', 'distances'] # documents are the 'text_for_embedding'
    )
    return results