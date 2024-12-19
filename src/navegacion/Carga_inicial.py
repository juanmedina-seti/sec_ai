import streamlit as st
import pandas as pd
import azure.identity
import json
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.schema.document import Document
import sys

from dotenv import load_dotenv
import os


load_dotenv()
sys.path.append(".")
from src.utils.get_embedding_function import get_embedding_function

from src.utils.log_settings import configure_logging

logger=configure_logging()
logger.info("Carga inicial.py")

FIELDS=['Id',"Pregunta", "Respuesta","Detalle","Tema","Categoria","Cliente","Fecha"]
vector_store_address = os.environ.get("AZURE_SEARCH_SERVICE")
vector_store_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")
excel_file_path = os.environ.get("EXCEL_FILE_PATH")
index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME") 

embedding_function = get_embedding_function(embedding_model)

# Streamlit app
st.header("Cargar desde Excel")

uploaded_file = st.file_uploader("Seleccione un archivo", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df.head())  # Display a preview of the data
        faltantes=[col for col in FIELDS if col not in df.columns]
        if len(faltantes) > 0:
            st.write(f"No se encontraron la(s) columna(s): {str(faltantes)}" )
            raise IndexError("Faltan columnas en el excel ")
        if not df["Id"].is_unique:
            raise ValueError("El id debe ser único ")
        
        vector_store = AzureSearch(
                azure_search_endpoint=vector_store_address,
                azure_search_key=vector_store_key,
                index_name=index_name,
                embedding_function=embedding_function,
            )


        documents = []
        ids = []
        for index, row in df.iterrows():
            # Generate a unique ID for each document
            doc_id = str(row["Id"])
            logger.debug("Doc ID",doc_id)
            # Process only rows with sufficient data in "Pregunta"
            if not pd.isna(row["Pregunta"]) and len(str(row["Pregunta"])) > 30 and not pd.isna(row["Detalle"]) and len(str(row["Detalle"])) >10: 
                content = str(row['Pregunta'])
                
                metadata = {
                    "respuesta": row["Respuesta"],
                    "detalle": row ["Detalle"],
                    "categoria": row["Categoria"],
                    "tema": row["Tema"],
                    "cliente": row["Cliente"],
                    "fecha": str(row["Fecha"]),
                }
                logger.debug("Metadata",row.to_list())
                documents.append(Document(page_content=content, metadata=metadata))
                logger.debug("Len",len(documents))
                ids.append(doc_id)

        if documents: # Check if any documents were created (handles empty files gracefully)
            batch_size = 30 # Adjust batch size as needed. Smaller values are safer if you have memory limitations.
            my_bar = st.progress(0, text="Cargando ...")
            for i in range(0, len(documents), batch_size):
               # st.info(f"Adding documents {i} to {min(i+batch_size, len(documents))}")
                vector_store.add_documents(documents=documents[i : i + batch_size], ids=ids[i : i + batch_size])
                my_bar.progress(int(i/len(documents)*100), text=f"Cargando de {i} a {min(i+batch_size, len(documents))} de {len(documents)}")
            my_bar.progress(100, text=f"Cargando")
            st.success(f"Successfully added {len(documents)} documents to the index.")

        else:
             st.warning("No documents were created. Make sure the Excel file is formatted correctly and contains data in the 'Pregunta' column.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
