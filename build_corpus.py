from newsapi.newsapi_client import NewsApiClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import uuid

TRUSTED_SOURCES = (
    "the-hindu",
    "the-times-of-india"
)

def fetch_news():
    load_dotenv()
    NEWS_API_KEY= os.getenv("NEWS_API_KEY")

    newsapi = NewsApiClient(NEWS_API_KEY)
    top_headlines = newsapi.get_top_headlines(sources=','.join(TRUSTED_SOURCES),
                                              language='en',)

    return top_headlines

def save_news():
    headlines = fetch_news()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"news_corpus_{timestamp}.jsonl"  # JSONL format for RAG
    filepath = os.path.join("data", "corpus", filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    corpus_entries = []
    
    for article in headlines['articles']:
            
        # Create unique document ID
        doc_id = str(uuid.uuid4())
        
        # Clean and prepare text content
        title = article['title'].strip()
        description = article['description'].strip() if article['description'] else ""
        content = article.get('content', '').strip() if article['content'] else ""
        
        # Combine for full document text
        full_text = f"{title}\n\n{description}"
        if content and content != description:  # Avoid duplication
            full_text += f"\n\n{content}"
        
        # RAG-optimized entry structure
        corpus_entry = {
            "id": doc_id,
            "text": full_text,
            "metadata": {
                "title": title,
                "source": article['source']['name'],
                "source_id": article['source']['id'],
                "author": article.get('author', 'Unknown'),
                "published_at": article['publishedAt'],
                "url": article['url'],
                "category": "news",
                "trustworthy": True,
                "language": "en",
                "added_at": datetime.now().isoformat(),
                "word_count": len(full_text.split()),
                "char_count": len(full_text)
            }
        }
        
        corpus_entries.append(corpus_entry)
    
    # Save in JSONL format (one JSON object per line)
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in corpus_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Saved {len(corpus_entries)} documents to {filepath}")


save_news()
