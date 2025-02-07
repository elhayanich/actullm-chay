from parse import embed_text
import chromadb
import ollama
import datetime

#chromasb
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("articles")

def get_today_date():
    return datetime.datetime.now().strftime("%d %B %Y")

def search_articles(query, n_results=5):
    query_vector = embed_text(query)  
    results = collection.query(query_embeddings=[query_vector], n_results=n_results)

    relevant_articles = []
    for result in results["metadatas"]:
        article = result[0]  
        relevant_articles.append({
            "title": article["title"],
            "summary": article["summary"],
            "link": article["link"],
            "published": article["published"]
        })
    
    return relevant_articles

#réponse avec articles
def generate_response_with_articles(query, relevant_articles):
    today_date = get_today_date()
    
    prompt = f"""Tu es un expert en actualités et nous sommes aujourd'hui le {today_date}.
Voici des articles récents concernant la question suivante : '{query}' :\n\n"""

    for article in relevant_articles:
        prompt += f"- **Titre**: {article['title']}\n"
        prompt += f"  **Résumé**: {article['summary']}\n"
        prompt += f"  **Date de publication**: {article['published']}\n"
        prompt += f"  **Lien**: {article['link']}\n\n"
    
    prompt += f"""En fonction des informations ci-dessus et en tenant compte du fait que nous sommes le {today_date}, réponds précisément à la question suivante :\n
**Question** : {query}\n
**Réponse** : Donne un résumé clair et précis en utilisant la date d’aujourd’hui comme référence."""

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    try:
        return response["message"]["content"]
    except KeyError:
        return "Aucune réponse texte n'a été générée."

#réponse sans articles
def generate_response_without_articles(query):
    today_date = get_today_date()
    
    prompt = f"""Tu es un expert en actualités et nous sommes aujourd'hui le {today_date}.
Réponds précisément à la question suivante en prenant en compte cette date :
    
**Question** : {query}
**Réponse** : Donne un résumé clair et précis."""

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    try:
        return response["message"]["content"]
    except KeyError:
        return "Aucune réponse texte n'a été générée."


