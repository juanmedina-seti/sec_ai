import streamlit as st

from langchain_community.vectorstores.azuresearch import AzureSearch

from dotenv import load_dotenv
import os
import sys


load_dotenv()  # Load the .env file
sys.path.append(".")
from src.utils.get_embedding_function import get_embedding_function
from src.utils.log_settings import configure_logging

logger = configure_logging()
logger.info("Busqueda.py")

vector_store_address = os.environ.get("AZURE_SEARCH_SERVICE")
vector_store_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME")
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")
search_type = os.environ.get("SEARCH_TYPE", "hybrid")  # Default to "hybrid" if not set

try:
    k_value = int(os.environ.get("K_VALUE", 2))
except ValueError:
    logger.error("Invalid K_VALUE environment variable. Using default value of 2.")
    k_value = 2


embedding_function = get_embedding_function(embedding_model)


db: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_key,
    index_name=index_name,
    embedding_function=get_embedding_function(embedding_model),
    #token_provider = token_provider
)

st.header("Analista de Seguridad SETI")

query_text = st.text_area("Ingrese la pregunta ")
if st.button("Enviar pregunta"):
    try:
        results = db.similarity_search(query_text, k=k_value+1, search_type=search_type)
        context_text = "\n\n---\n\n".join(
            [f"{doc.page_content}:  {doc.metadata['detalle']}" for doc in results]
        )
        st.header("Preguntas similares")
        results.sort(key=lambda doc: doc.metadata.get("fecha"), reverse=True)
        for doc in results[:-1]:
            with st.expander("", expanded=True):
                st.markdown(f"**{doc.metadata.get('pregunta', 'N/A')}**")
                st.markdown(f"**Respuesta:** {doc.metadata.get('respuesta', 'N/A')}")
                st.markdown(f"**Detalle:** {doc.metadata.get('detalle', 'N/A')}")
                st.markdown(f"**Fecha:** {doc.metadata.get('fecha', 'N/A')}")
                st.markdown(f"**Cliente:** {doc.metadata.get('cliente', 'N/A')}")
                st.markdown(f"**Tema:** {doc.metadata.get('tema', 'N/A')}")
                st.markdown(f"**Categoría:** {doc.metadata.get('categoria', 'N/A')}")
    except Exception as e:
        logger.exception(f"An error occurred during search: {e}")
        st.error(f"An error occurred: {e}")

