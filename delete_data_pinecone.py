from pinecone import Pinecone
import os
from dotenv import load_dotenv

def delete_data_pinecone():
    load_dotenv()

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("ihk-pdf")

    index.delete(delete_all=True, namespace='PDF')

if __name__ == '__main__':
    delete_data_pinecone()
