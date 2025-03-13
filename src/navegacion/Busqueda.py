import streamlit as st
#from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate
#from langchain_google_genai import ChatGoogleGenerativeAI

import azure.identity
from langchain_community.vectorstores.azuresearch import AzureSearch

from dotenv import load_dotenv
import os
import sys

load_dotenv()  # Load the .env file
sys.path.append(".")
from src.utils.get_embedding_function import get_embedding_function
from src.utils.log_settings import configure_logging

logger=configure_logging()
logger.info("Busqueda.py")

vector_store_address = os.environ.get("AZURE_SEARCH_SERVICE")
vector_store_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME") 
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")


search_type=st.selectbox("Tipo Consulta",["hybrid","similarity"])    
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
if(st.button("Enviar pregunta")):
    
        results = db.similarity_search(query_text, k=2,search_type=search_type)
        
        context_text = "\n\n---\n\n".join([f"{doc.page_content}:  {doc.metadata['detalle']}" for doc in results])
        #sources = "\n\n---\n\n".join([f"{doc.metadata['filename']}:{doc.metadata['line_number']}:" for doc, _score in results])
        st.header("Preguntas similares") 
        for doc in results:
            

            # Use expander to show details (collapsible)
            with st.expander("",expanded=True):
                st.markdown(f"**{doc.metadata.get('pregunta', 'N/A')}**")  # Make question a subheader
                st.markdown(f"**Respuesta:** {doc.metadata.get('respuesta', 'N/A')}")  # Handle missing data
                st.markdown(f"**Detalle:** {doc.metadata.get('detalle', 'N/A')}")
                st.markdown(f"**Fecha:** {doc.metadata.get('fecha', 'N/A')}")
                st.markdown(f"**Cliente:** {doc.metadata.get('cliente', 'N/A')}")
                st.markdown(f"**Tema:** {doc.metadata.get('tema', 'N/A')}")
                st.markdown(f"**Categoría:** {doc.metadata.get('categoria', 'N/A')}")

        #prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        #prompt = prompt_template.format(context=context_text, question=query_text)
        #response_text = model.invoke(prompt)
        #st.header("Respuesta a partir del contexto")
        #st.write(response_text.content)
