
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

from dotenv import load_dotenv
import os


load_dotenv()


# Azure Search service endpoint and key

embedding_model = os.environ.get("EMBEDDING_MODEL_QA")



def get_embedding_function(model=embedding_model):


    
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",

    )

    return embeddings

