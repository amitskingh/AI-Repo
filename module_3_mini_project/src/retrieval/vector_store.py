from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.ingestion.chunk_documents import split_documents
from src.ingestion.load_documents import load_documents


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_store():
    documents = load_documents()
    chunks = split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="hoa_documents",
        persist_directory="data/chroma",
    )

    return vector_store


if __name__ == "__main__":
    vector_store = create_vector_store()
    # print(vector_store)
    print("Vector store created.")
    query = "How much can I be fined?"

    results = vector_store.similarity_search(
        query,
        k=3,
    )

    for result in results:
        print("=" * 60)
        print(result.page_content)
        print(result.metadata)