from pathlib import Path

from langchain_community.document_loaders import TextLoader


DOCUMENTS_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        loader = TextLoader(file_path)
        documents.extend(loader.load())

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print("=" * 60)
        print(document.page_content)
        print(document.metadata)