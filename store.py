import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings  
from langchain_community.docstore.document import Document
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import DirectoryLoader
from dotenv import load_dotenv
import openai
import os
import pinecone
from langchain.vectorstores import Pinecone as PineconeVectorStore

load_dotenv()

class vector_DB:
    def __init__(self) -> None:
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
        # Initialize Pinecone client
        self.pinecone_client = Pinecone(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        self.index_name = "ihk-pdf"
        # self.model_name = 'text-embedding-ada-002'
        # self.embed = OpenAIEmbeddings(model=self.model_name, openai_api_key=os.environ.get("OPENAI_API_KEY"))
        # Check and create index
        # self._check_and_create_index()

    # def _check_and_create_index(self):
    #     # Call the list_indexes method and access its result
    #     index_list = self.pinecone_client.list_indexes()
    #     # Depending on the Pinecone client's return type, you might need to access the names differently
    #     # Assuming it returns a dictionary or an object with a 'names' attribute that is a list or iterable
    #     index_names = index_list.names if hasattr(index_list, 'names') else []
        
    #     if self.index_name not in index_names:
    #         self.pinecone_client.create_index(
    #             name=self.index_name,
    #             dimension=1536,  # Update this based on your embedding dimension
    #             metric='cosine',  # Choose 'cosine' or 'euclidean' based on your need
    #             spec=ServerlessSpec(cloud='gcp-starter', region='us-central-1')  # Update cloud and region if needed
    #         )
    # def pinecone(self):
    #     pinecone.init(
    #     api_key=self.PINECONE_API_KEY,
    #     environment=self.PINECONE_ENV
    # )


    def load_docs(self, directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents

    def split_docs(self, documents, chunk_size=2500, chunk_overlap=150):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        print(f"{len(docs)} chunks created.")
        return docs

    def pdf_embedding(self):
        print("Processing PDF file..")

        pdf_directory = "Output/From_PDF/Text"
        documents = self.load_docs(pdf_directory)
        docs = self.split_docs(documents)
        # obj.pinecone_client(Pinecone(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV))

        print("Creating Embeddings..")
        data = PineconeVectorStore.from_documents(docs, self.embeddings, index_name=self.index_name, namespace="PDF" )
        # Update this section to use the pinecone_client for indexing
        # You might need to adjust the method calls based on the Pinecone SDK's documentation

        print("PDF embeddings stored successfully.")
        # Consider adding cleanup or additional functionality as needed

    # def xls_embedding(self):
    #     print("Processing XLS file..")

    #     xls_directory = "src/Output/From_XLS/Text"
    #     documents = obj.load_docs(xls_directory)
    #     docs = obj.split_docs(documents)
    #     obj.pinecone()

    #     print("Creating Embeddings..")
    #     data = Pinecone.from_documents(docs, self.embeddings, index_name=self.index_name, namespace="XLS" )
    #     print("XLS embeddings stored successfully.")

    #     # data.delete(delete_all=True, namespace="XLS")
    #     # print("Data deleted.")

    # def xls_category(self):
        # categories = ["Biscuits","Candies","Chocolate","Salty_Snacks"]
        # marketers = ["Edeka", "Globus", "Kaufland", "National", "ReweNational"]
        # arr=[]

        # for category in categories:
        #     for market in marketers:
        #         xls_directory = f"src/Output/From_XLS/Category/{category}/{market}"
        #         documents = self.load_docs(xls_directory)
        #         arr.append(documents[0])
        
        # self.pinecone()
        # print("Creating Embeddings..")
        # print(f"{len(arr)} embeddings created")
        # data = Pinecone.from_documents(arr, self.embeddings, index_name=self.index_name, namespace="XLS" )
        # print("XLS embeddings stored successfully.")

def main_store():
    obj = vector_DB()
    obj.pdf_embedding()

if __name__ == "__main__":
    main_store()
