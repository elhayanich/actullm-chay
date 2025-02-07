import feedparser
import ssl
import ollama
from datetime import timezone, datetime
import dateutil.parser  

ssl._create_default_https_context = ssl._create_unverified_context

rss_urls = [
    "https://www.france24.com/fr/europe/rss",
    "https://www.france24.com/fr/afrique/rss",
    "https://www.france24.com/fr/am%C3%A9riques/rss",
    "https://www.france24.com/fr/moyen-orient/rss",
    "https://www.france24.com/fr/asie-pacifique/rss"
]

#embedding func
def embed_text(text):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

def parse_rss():
    articles = []
    today = datetime.now(timezone.utc).date()

    for rss_url in rss_urls:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            published_str = entry.get("published", "")
            try:
                published_date = dateutil.parser.parse(published_str).date()
            except (ValueError, TypeError):
                continue 

            if published_date == today:
                article = {
                    "title": entry.get("title", ""),
                    "published": published_str,
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", "")
                }
                articles.append(article)
    
    return articles

# verif
# if __name__ == "__main__":
#     articles = parse_rss()

#     if articles:
#         print("Articles récupérés aujourd'hui :")
#         for i, article in enumerate(articles):
#             print(f"\n🔹 Article {i + 1}:")
#             print(f"   - **Titre**: {article['title']}")
#             print(f"   - **Date de publication**: {article['published']}")
#             print(f"   - **Résumé**: {article['summary']}")
#             print(f"   - **Lien**: {article['link']}")
#     else:
#         print("Aucun article publié aujourd'hui.")



