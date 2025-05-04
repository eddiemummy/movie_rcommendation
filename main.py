from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st

api_key = st.secrets["GOOGLE_GEMINI_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)


prompt = PromptTemplate(
    input_variables=["genre", "paragraph", "language"],
    template="Can you recommend a movie that has the genre {genre} and summarize the movie in {paragraph} short paragraph(s) in the language {language}.",
)
st.title("Movie Recommendation")
genre = st.text_input("Genre")
paragraph = st.number_input("Summary: Input Number of Paragraphs", min_value=1, max_value=5)
language = st.text_input("Language")

if genre and paragraph and language:
    query = prompt.format(genre=genre, paragraph=paragraph, language=language)
    response = llm.invoke(query)
    content = response.content  

    if "</think>" in content:
        final_output = content.split("</think>")[-1].strip()
    else:
        final_output = content.strip()

    st.subheader("Response:")
    st.write(final_output)


