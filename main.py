from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st

api_key = st.secrets["GOOGLE_GEMINI_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)


prompt = PromptTemplate(
    input_variables=["genre", "paragraph", "language", "min_rating", "excluded_clause"],
    template=(
        "Recommend a lesser-known but high-quality movie in the {genre} genre with an IMDb rating of at least {min_rating}. "
        "Do not repeat the same suggestions. Recommend a movie in the {genre} genre with an IMDb rating of at least {min_rating}. "
        "{excluded_clause}"
        "Avoid blockbuster or overly popular mainstream titles. Prioritize hidden gems, festival favorites, international cinema, or auteur-directed works "
        "that are critically acclaimed but not widely known. "
        "Summarize the recommended film in {paragraph} short paragraph(s) in {language}."
    ),
)

st.title("🎬 Movie Recommendation")

genre = st.text_input("🎭 Genre")
paragraph = st.number_input("📝 Summary: Number of Paragraphs", min_value=1, max_value=5)
language = st.text_input("🌍 Language")
min_rating = st.number_input("⭐️ Minimum IMDb Rating", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
excluded_input = st.text_input("🚫 Exclude These Movies (Separate titles with commas)")

if genre and paragraph and language:
    excluded_list = ", ".join([movie.strip() for movie in excluded_input.split(",") if movie.strip()])
    excluded_clause = f"Exclude the following movies from your recommendation: {excluded_list}. " if excluded_list else ""

    query = prompt.format(
        genre=genre,
        paragraph=paragraph,
        language=language,
        min_rating=min_rating,
        excluded_clause=excluded_clause
    )

    response = llm.invoke(query)
    content = response.content

    if "</think>" in content:
        final_output = content.split("</think>")[-1].strip()
    else:
        final_output = content.strip()

    st.subheader("🎥 Recommended Movie:")
    st.write(final_output)
