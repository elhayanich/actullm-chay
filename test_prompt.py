import chromadb
import ollama
from parse import embed_text 

# Création de la base de données pour le test
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("articles")

def search_articles(query, n_results=3):
    query_vector = embed_text(query)  
    results = collection.query(
        query_embeddings=[query_vector],  
        n_results=n_results  
    )

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

# Fonction pour générer la réponse en incluant les articles dans le prompt
def generate_response_with_articles(query, relevant_articles):
    prompt = f"Voici des articles récents concernant ta question '{query}' :\n\n"

    for article in relevant_articles:
        prompt += f"- **Titre**: {article['title']}\n"
        prompt += f"  **Résumé**: {article['summary']}\n"
        prompt += f"  **Date de publication**: {article['published']}\n"
        prompt += f"  **Lien**: {article['link']}\n\n"
    
    prompt += f"En fonction des informations ci-dessus, réponds à la question suivante :\n"
    prompt += f"**Question** : {query}\n"
    prompt += f"**Réponse** : Donne un résumé clair et précis."

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    try:
        return response["message"]["content"]
    except KeyError:
        return "Aucune réponse texte n'a été générée."

# Fonction pour générer la réponse sans inclure les articles dans le prompt
def generate_response_without_articles(query):
    prompt = f"**Question** : {query}\n"
    prompt += f"**Réponse** : Donne un résumé clair et précis."

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    try:
        return response["message"]["content"]
    except KeyError:
        return "Aucune réponse texte n'a été générée."

# Fonction de test
def test_responses(query):
    # Recherche d'articles pertinents
    relevant_articles = search_articles(query)

    if relevant_articles:
        # Réponse avec les articles dans le prompt
        response_with_articles = generate_response_with_articles(query, relevant_articles)
        print("Réponse avec les articles dans le prompt :")
        print(response_with_articles)
        print("\n" + "="*50 + "\n")
        
        # Réponse sans les articles dans le prompt
        response_without_articles = generate_response_without_articles(query)
        print("Réponse sans les articles dans le prompt :")
        print(response_without_articles)
    else:
        print("Aucun article pertinent trouvé.")

# Main function pour tester
def main():
    query = input("Quel est ta question ? ")  
    test_responses(query)

if __name__ == "__main__":
    main()
