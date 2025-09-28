import json

def load_corpus(filepath):
    """Helper function to load corpus for RAG system"""
    documents = []
    metadatas = []
    ids = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            documents.append(entry['text'])
            metadatas.append(entry['metadata'])
            ids.append(entry['id'])
    
    return {
        "documents": documents,
        "metadatas": metadatas,
        "ids": ids
    }