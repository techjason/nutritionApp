import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from PIL import Image
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="中風患者飲食顧問", page_icon="🧠", layout="centered", initial_sidebar_state="auto", menu_items=None)

# This makes page look better, but it is unsafe
st.markdown('''<style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .css-1vq4p4l.e1fqkh3o4 {margin-top: -75px;}''', unsafe_allow_html=True)


image = Image.open('hkustrokelogo.png')
st.image(image, width=300)

openai.api_key = st.secrets.openai_key
st.title("🧠 中風患者飲食顧問")
st.info("這款AI是在HKUStroke的專業營養師驗證的[特定材料](https://docs.google.com/document/d/10DaTtRame1k0FkivbK23GUsGJhgW4ADoRYw4H55vt8M/edit#heading=h.nlh5g19s3ps3)上進行培訓的，儘管如此，有時AI可能會給出不准確的回應。", icon="❗️")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "隨便問我關於中風患者營養和食物的問題！"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1, system_prompt="You are an expert nutritionist for stroke patients and your job is to answer questions regarding nutrition for stroke patients. Assume that all questions are from post-stroke patients. Do not hallucinate features. You must respond in Traditional Chinese."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()
# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
