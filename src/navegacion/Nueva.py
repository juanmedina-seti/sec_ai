import streamlit as st
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import sys


load_dotenv()

sys.path.append(".")
from src.utils.get_embedding_function import get_embedding_function
from src.utils.log_settings import configure_logging

logger=configure_logging()
logger.info("Nueva.py")
# Azure Search service endpoint and key
service_endpoint = os.environ.get("AZURE_SEARCH_SERVICE")
key = os.environ.get("AZURE_SEARCH_KEY")
index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME") 
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")


# Initialize the search client
credential = AzureKeyCredential(key)
search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)


embedding_function = get_embedding_function(embedding_model)


# CRUD Operations

# Create
st.header("Nueva pregunta")
with st.form("create_form"):
    pregunta = st.text_input("Pregunta")
    respuesta = st.text_input("Respuesta")
    detalle = st.text_area("Detalle")
    categoria = st.text_input("Categoria")
    tema = st.text_input("Tema")
    cliente = st.text_input("Cliente")
    fecha = st.date_input("Fecha")
    create_submitted = st.form_submit_button("Crear")

    if create_submitted:
        vector = embedding_function([pregunta])  # Generate embedding
        metadata = {
            "respuesta": respuesta,
            "detalle": detalle,
            "categoria": categoria,
            "tema": tema,
            "cliente": cliente,
            "fecha": fecha.isoformat(), # Store as string
        }        
        document = {
            "content": pregunta,
            "metadata": metadata,
            "content_vector": vector # Add the embedding to the document
        }
        try:
            result = search_client.upload_documents([document])
            st.success(f"Document created with key: {result[0].key}")
        except Exception as e:
            st.error(f"Error creating document: {e}")


