# decomment the code you want to run for the streamlit app the first is ollama and the second is openai

######## Ollama streamlit ########


import streamlit as st
from prompt import search_articles, generate_response_with_articles, generate_response_without_articles

def main():
    st.markdown('<div class="header">ACTULLM CHAY</div>', unsafe_allow_html=True)

    # Input from the user
    user_question = st.text_input("Pose ta question, please !", key="question_input")

    if user_question:
        with st.spinner('Recherche des articles...'):
            relevant_articles = search_articles(user_question)

            if relevant_articles:

                response_with_articles = generate_response_with_articles(user_question, relevant_articles)
                response_without_articles = generate_response_without_articles(user_question)
                st.chat_message("user").markdown(f"**Question**: {user_question}")
                st.chat_message("assistant").markdown(f"**Réponse avec les articles dans le prompt**:\n{response_with_articles}")
                st.chat_message("assistant").markdown(f"**Réponse sans les articles dans le prompt**:\n{response_without_articles}")
            else:
                st.chat_message("assistant").markdown("Aucun article pertinent trouvé.")

if __name__ == "__main__":
    main()


######## OpenAI streamlit ########

# import streamlit as st
# from prompt import search_articles, generate_response_with_articles, generate_response_without_articles

# # Custom CSS for styling
# st.markdown(
#     """
#     <style>
#         .header {
#             font-size: 24px;
#             font-weight: bold;
#             text-align: center;
#             margin-bottom: 20px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# def main():
#     st.markdown('<div class="header">ACTULLM CHAY</div>', unsafe_allow_html=True)

#     # Input from the user
#     user_question = st.text_input("Pose ta question, please !", key="question_input")

#     if user_question:
#         with st.spinner('🔎 Recherche des articles...'):
#             relevant_articles = search_articles(user_question)

#         # Streamlit chat UI
#         st.chat_message("user").markdown(f"**Question**: {user_question}")

#         if relevant_articles:
#             with st.spinner("réponse avec GPT-4o-mini..."):
#                 response_with_articles = generate_response_with_articles(user_question, relevant_articles)
#                 response_without_articles = generate_response_without_articles(user_question)

#             # Display responses
#             st.chat_message("assistant").markdown(f"**Réponse avec les articles**:\n{response_with_articles}")
#             st.chat_message("assistant").markdown(f"**Réponse sans les articles**:\n{response_without_articles}")
#         else:
#             st.chat_message("assistant").markdown("⚠️ Aucun article pertinent trouvé.")

# if __name__ == "__main__":
#     main()
