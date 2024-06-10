import streamlit as st
import ollama

def generate_response():
    response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

st.title ("Want some help choosing a holiday?)
st.header("Give us an idea of what you like.")

with st.container():
        query = st.text_area("My ideal holiday is..", height= 100, key= "query_text")
        button = st.button("Submit", key="button")

st.write('The entered text is:', query)

