import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI 
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import huggingface_hub

# Function to extract text from uploaded PDF documents
def load_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split the extracted text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Function to create a FAISS vector store from text chunks
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    
    # Add only the new messages to the chat history
    new_ai_message = response['chat_history'][-1].content
    
    # Add the user's question and AI's response to the messages
    st.session_state.messages.append({"role": "user", "content": user_question})
    st.session_state.messages.append({"role": "assistant", "content": new_ai_message})
    
    # Display only the new messages
    with st.chat_message("user"):
        st.markdown(user_question)
    with st.chat_message("assistant"):
        st.markdown(new_ai_message)

# Main function to run the Streamlit application
def run_chatbot():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)

    st.title("📚 AML Assistant")
    st.write(
        "This chatbot uses OpenAI's GPT model to answer questions about your AML documents. "
        "Select a procedure and ask questions about it."
    )

    # Procedure selection
    procedure_options = {
        "AML": "procedures/AML FATF.pdf",
        "PEP": "procedures/PEP FATF Procedure.pdf",
        "Sanctions": "procedures/World Bank Sanctions Procedure.pdf"
    }
    selected_procedure = st.radio("", list(procedure_options.keys()), horizontal=True)
    
    if st.button("Process"):
        with st.spinner("Processing"):
            pdf_path = procedure_options[selected_procedure]
            raw_text = load_pdf(pdf_path)
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            st.session_state.conversation = get_conversation_chain(vectorstore)
            st.success(f"{selected_procedure} procedure successfully!")

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the selected procedure:"):
        if st.session_state.conversation:
            handle_userinput(prompt)
        else:
            st.warning("Please select and process a procedure before asking questions.")

    st.markdown("""
    <div style='text-align: center; color: gray; margin-top: 10px;'>
        <em>AML Assistant can make mistakes. Please verify the information and consult with a professional when in doubt.</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    run_chatbot()