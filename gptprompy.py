import os
import requests
import json
import chromadb
import datetime
from dotenv import load_dotenv
from parse import embed_text  


load_dotenv()

# azure oai maxime
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")


#chromaDB
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

def call_azure_gpt4(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }

    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
        "model": AZURE_DEPLOYMENT_NAME  
    }

    try:
        response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
        response_data = response.json()

        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            return f"Erreur : Réponse inattendue de l'API - {response_data}"
    
    except Exception as e:
        return f"Erreur lors de l'appel à l'API Azure OpenAI: {e}"

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

    return call_azure_gpt4(prompt)

def generate_response_without_articles(query):
    today_date = get_today_date()
    
    prompt = f"""Tu es un expert en actualités et nous sommes aujourd'hui le {today_date}.
Réponds précisément à la question suivante en prenant en compte cette date :
    
**Question** : {query}
**Réponse** : Donne un résumé clair et précis."""

    return call_azure_gpt4(prompt)

#tets
if __name__ == "__main__":
    test_query = "Quels sont les événements marquants d'aujourd'hui ?"
    articles = search_articles(test_query)

    if articles:
        print("Réponse avec articles:")
        print(generate_response_with_articles(test_query, articles))
    else:
        print("Réponse sans articles:")
        print(generate_response_without_articles(test_query))


