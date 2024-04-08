import json
import shutil
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
        self.pinecone_client = Pinecone(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        self.index_name = "ihk-pdf"

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

        print("Creating Embeddings..")
        data = PineconeVectorStore.from_documents(docs, self.embeddings, index_name=self.index_name, namespace="PDF" )
        print("PDF embeddings stored successfully.")

        # Copy contents and clear the source file at the end
        source_file = os.path.join(pdf_directory, "post_formatted_text.txt")
        dest_file = os.path.join("Output/From_PDF/unused_text", "post_formatted_text.txt")
        self.copy_and_clear_file(source_file, dest_file)

    def copy_and_clear_file(self, source, destination):
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Copy the file
        shutil.copyfile(source, destination)
        print(f"Contents copied from {source} to {destination}.")

        # Clear the contents of the source file
        with open(source, 'w') as file:
            file.truncate(0)
        print(f"Contents of {source} cleared.")

def main_store():
    obj = vector_DB()
    obj.pdf_embedding()

if __name__ == "__main__":
    main_store()
