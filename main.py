from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st
import random
from datetime import datetime

api_key = st.secrets["GOOGLE_GEMINI_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    google_api_key=api_key,
    temperature=0.5 
)


if "suggested_movies" not in st.session_state:
    st.session_state.suggested_movies = []

if "trigger_new" not in st.session_state:
    st.session_state.trigger_new = False


st.title("🎬 Movie Recommendation")
st.markdown("""
### ℹ️ Açıklama / About

💡 **Önerilen film listesi** geçici olarak tarayıcı belleğinde saklanır. Bu sayede aynı filmi tekrar önermemeye çalışır.  
🔄 "Refresh Recommendation" butonuna tıklayarak aynı ayarlarla yeni bir film önerisi alabilirsiniz.  
🌐 Sayfayı yenilerseniz önceki öneriler sıfırlanır.

---

💡 The **suggested movies** are temporarily stored in your browser's memory during this session  
🔄 You can click the "Refresh Recommendation" button to get a new recommendation using the same filters.  
🌐 If you refresh the page, the previous suggestions will be cleared.
""")


genre = st.text_input("🎭 Genre")
paragraph = st.number_input("📝 Summary: Number of Paragraphs", min_value=1, max_value=5)
language = st.text_input("🌍 Language")
min_rating = st.number_input("⭐️ Minimum IMDb Rating", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
manual_exclude = st.text_input("🚫 Exclude These Movies (comma separated)")

variety_hints = [
    # topics
    "prefer underrepresented regions",
    "focus on female directors",
    "explore post-2000 films only",
    "prioritize debut movies",
    "avoid time travel tropes",
    "think outside Hollywood",
    "include LGBTQ+ themed stories",
    "prefer movies with minimal dialogue",
    "recommend films with non-linear narratives",
    "favor experimental cinematography",
    "consider low-budget indie productions",
    "suggest movies that received festival awards but not mainstream success",
    "highlight works from politically unstable countries",
    "explore regional language films",
    "recommend non-English movies only",
    "avoid Oscar-winning films",
    "prefer movies that blur genre boundaries",
    "select films with unknown or amateur actors",
    "recommend animated films for adult audiences",
    "focus on psychological or philosophical themes",
    
    # regions
    "recommend only Asian films",
    "recommend only European films",
    "recommend only South American films",
    "prefer films from Southeast Asia",
    "focus on Eastern European cinema",
]

if st.button("🔄 Refresh Recommendation"):
    st.session_state.trigger_new = True

if genre and paragraph and language and st.session_state.trigger_new:
    st.session_state.trigger_new = False 

    excluded_list = [movie.strip() for movie in manual_exclude.split(",") if movie.strip()]
    excluded_list += st.session_state.suggested_movies
    excluded_clause = (
        f"Exclude the following movies: {', '.join(set(excluded_list))}. " if excluded_list else ""
    )

    random_hint = random.choice(variety_hints)

    prompt_template = PromptTemplate(
        input_variables=["genre", "paragraph", "language", "min_rating", "excluded_clause", "variety_hint"],
        template=(
            "Please do NOT start with commonly suggested movies.\n"
            "Recommend a unique, lesser-known but high-quality movie in the {genre} genre with an IMDb rating of at least {min_rating}. "
            "{excluded_clause}"
            "Avoid overly mainstream or over-recommended films. Instead, {variety_hint}. "
            "Summarize the recommended film in {paragraph} short paragraph(s) in {language}."
        )
    )

    query = prompt_template.format(
        genre=genre,
        paragraph=paragraph,
        language=language,
        min_rating=min_rating,
        excluded_clause=excluded_clause,
        variety_hint=random_hint
    )

    response = llm.invoke(query)
    content = response.content.strip()

    if "</think>" in content:
        content = content.split("</think>")[-1].strip()

    first_line = content.splitlines()[0]
    if first_line:
        movie_title = first_line.split(".")[0].strip("–-•* ")
        if movie_title and movie_title not in st.session_state.suggested_movies:
            st.session_state.suggested_movies.append(movie_title)

    st.subheader("🎥 Recommended Movie:")
    st.write(content)
