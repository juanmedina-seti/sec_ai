# Base_de_datos.py (Integrated Search, Edit, Delete)

import streamlit as st
import pandas as pd
import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import sys

load_dotenv()
sys.path.append(".")  # Ensure src is in path
from src.utils.get_embedding_function import get_embedding_function

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


# Read (Search)
st.header("Buscar pregunta")
with st.form("search_form"):
    search_query = st.text_input("Consulta")
    search_button = st.form_submit_button("Buscar")

    if search_button:
        try:
            results = search_client.search(search_text=search_query, include_total_count=True)
            total_count = results.get_count()
            st.write(f"Total resultados: {total_count}")

            if total_count > 0:
                df = pd.DataFrame([result for result in results])
                st.dataframe(df)  # Display results

                # Add edit/delete buttons for each row
                for index, row in df.iterrows():
                    key = row["id"]
                    col1, col2, col3 = st.columns([1, 1, 1]) # For better layout of buttons
                    with col1:
                        if st.button(f"Editar ({key})"):
                            # Open the edit form with pre-filled data (using a modal or a new page)
                            st.write(f"Editando documento con clave: {key}")
                            # Add code here to open a modal or navigate to another page for editing
                            # ... (see edit form below) ...

                    with col2:
                        if st.button(f"Eliminar ({key})"):
                            try:
                                search_client.delete_documents([{"id": key}])
                                st.success(f"Documento {key} eliminado.")
                            except Exception as e:
                                st.error(f"Error eliminando el documento: {e}")

            else:
                st.info("No se encontraron resultados.")

        except Exception as e:
            st.error(f"Error buscando documentos: {e}")


# --- EDIT FORM (can be part of a modal or another page) ---
# This is a sample edit form.  Adjust as needed to fit your modal/page design.
# The keys from the selected row should be passed to pre-fill this form.

# You'll need to integrate this into the edit button's action.

def edit_document(document_key):
    try:
        document = search_client.get_document(key=document_key)
        st.write("Documento encontrado:")
        st.write(document)

            # Update fields (using the existing document as a template)
        with st.form("update_inner_form"):
                updated_document = document
                updated_document["content"] = st.text_input("Pregunta", value=document["content"])
                metadata:dict = json.loads(updated_document["metadata"])
                for field in [ "respuesta", "detalle", "categoria", "tema", "cliente"]:
                    if field in metadata.keys():
                        metadata[field] = st.text_input(field.capitalize(), value=document[field])
                metadata['fecha'] = st.date_input("Fecha", value= updated_document['fecha']).isoformat()
                update_button = st.form_submit_button("Update Document")

                if update_button:

                    updated_vector = embedding_function([updated_document['content']])
                    updated_document['content_vector'] = updated_vector
                    updated_vector["metadata"] = json.dumps(metadata)
                    result = search_client.merge_or_upload_documents([updated_document])
                    st.success(f"Document updated: {result[0].key}")


    except Exception as e:
            st.error(f"Error getting or updating document: {e}")

