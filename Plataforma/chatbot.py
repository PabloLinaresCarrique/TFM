import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import huggingface_hub
from utils import get_s3_client  # Import S3 client setup
from pdf_viewer import run_pdf_viewer_module
import io  # Import io for handling PDF in memory

# Function to extract text from PDF documents stored in S3
def load_pdf_from_s3(bucket_name, pdf_key):
    s3_client = get_s3_client()
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=pdf_key)
        pdf_data = response['Body'].read()
        pdf_reader = PdfReader(io.BytesIO(pdf_data))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error retrieving PDF from S3: {e}")
        return None

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

    st.title("📚 AML Assistant")
    st.write(
        "This chatbot uses LLM and RAG Technology to answer questions about documents. "
        "Select a procedure and ask questions about it."
    )

    # Procedure selection with S3 keys
    procedure_options = {
        "AML": "AML FATF.pdf",
        "PEP": "PEP FATF Procedure.pdf",
        "Sanctions": "World Bank Sanctions Procedure.pdf"
    }
    selected_procedure = st.radio("", list(procedure_options.keys()), horizontal=True)
    
    if st.button("Process"):
        with st.spinner("Processing"):
            # Retrieve the PDF content from S3
            pdf_key = procedure_options[selected_procedure]
            raw_text = load_pdf_from_s3('cortexneural-platform-images', pdf_key)  # Use your actual bucket name
            if raw_text:
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success(f"{selected_procedure} procedure loaded successfully!")
            else:
                st.error("Failed to load the procedure from S3.")

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
    
    # PDF viewer
    pdf_key = procedure_options.get(selected_procedure, "AML FATF.pdf")
    run_pdf_viewer_module('cortexneural-platform-images', pdf_key)  # Use your actual bucket name

    st.markdown("""
    <div style='text-align: center; color: gray; margin-top: 10px;'>
        <em>AML Assistant can make mistakes. Please verify the information and consult with a professional when in doubt.</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    run_chatbot()
