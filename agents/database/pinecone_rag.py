# agents/database/pinecone_rag.py

from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings

class KnowledgeGraph:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings()
        self.index = Pinecone.from_existing_index(
            index_name = "exom-kg",
            embedding = self.embeddings
        )

    def add_market_data(self, text):

        self.index.add_texts([text])