from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st

api_key = st.secrets["GOOGLE_GEMINI_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)


prompt = PromptTemplate(
    input_variables=["genre", "paragraph", "language", "min_rating", "excluded"],
    template=(
        "Can you recommend a movie in the {genre} genre "
        "with an IMDb rating of at least {min_rating}, "
        "excluding the movie titled '{excluded}', "
        "and summarize it in {paragraph} short paragraph(s) "
        "in {language}?"
    ),
)

st.title("🎬 Movie Recommendation")

genre = st.text_input("🎭 Genre")
paragraph = st.number_input("📝 Summary: Number of Paragraphs", min_value=1, max_value=5)
language = st.text_input("🌍 Language")
min_rating = st.number_input("⭐️ Minimum IMDb Rating", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
excluded = st.text_input("🚫 Exclude This Movie (Exact title)")

if genre and paragraph and language and min_rating and excluded:
    query = prompt.format(
        genre=genre,
        paragraph=paragraph,
        language=language,
        min_rating=min_rating,
        excluded=excluded
    )
    response = llm.invoke(query)
    content = response.content

    if "</think>" in content:
        final_output = content.split("</think>")[-1].strip()
    else:
        final_output = content.strip()

    st.subheader("🎥 Recommended Movie:")
    st.write(final_output)


