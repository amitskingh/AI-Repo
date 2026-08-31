from pathlib import Path

from langchain_community.document_loaders import TextLoader

from src.ingestion.document_metadata import DOCUMENT_METADATA


DOCUMENTS_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        loader = TextLoader(file_path)
        loaded_documents = loader.load()

        metadata = DOCUMENT_METADATA[file_path.name]

        for document in loaded_documents:
            document.metadata.update(metadata)

        documents.extend(loaded_documents)

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print("=" * 60)
        print(document.page_content)
        print(document.metadata)
