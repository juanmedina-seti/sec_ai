import streamlit as st
import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
from azure.search.documents.indexes import SearchIndexClient
import sys


load_dotenv()
sys.path.append(".")

from src.utils.log_settings import configure_logging

logger=configure_logging()
logger.info("azuresearch.py")
# Azure Search configuration (from environment variables)
service_endpoint = os.environ.get("AZURE_SEARCH_SERVICE")
admin_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME")


def get_index_status(index_name):
    """Gets the status of an Azure Search index."""
    try:
        logger.info(f"Get Index {index_name}")
        credential = AzureKeyCredential(admin_key)
        index_client = SearchIndexClient(endpoint=service_endpoint,  credential=credential)
        index_info  = index_client.get_index_statistics(index_name)
        return index_info

    except ResourceNotFoundError:
        return "Index not found"
    except Exception as e:
        return f"Error: {e}"



def delete_index(index_name):
    """Deletes an Azure Search index."""
    try:
        logger.info(f"Delete Index {index_name}")
        credential = AzureKeyCredential(admin_key)
        index_client = SearchIndexClient(endpoint=service_endpoint,  credential=credential)
        index_client.delete_index(index_name)
        logger.info("Index deleted successfully")
        return "Index deleted successfully"
    except ResourceNotFoundError:
        logger.error("Index not found")
        return "Index not found"
    except HttpResponseError as e:
        logger.error(f"Error deleting index: {e.message}")
        return f"Error deleting index: {e.message}"
    except Exception as e:
        logger.error(f"Error deleting index: {e.message}")
        return f"An unexpected error occurred: {e}"


st.header("Azure Search Index Management")

if index_name: #only run if index name is defined in .env
    index_status=get_index_status(index_name)
    st.write(f"Index Name: {index_name}")
    if type(index_status) == dict:
        st.write(f"Documentos: {index_status["document_count"]}")
        if st.button("Delete Index"):
            result = delete_index(index_name)
            st.write(result)
            st.rerun()
        
       
    else:
        st.error(index_status)

else:
    logger.error("Index name not specified in environment variables.")
    st.error("Index name not specified in environment variables.")


