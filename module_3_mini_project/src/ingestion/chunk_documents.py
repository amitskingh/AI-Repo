from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40,
    )

    return splitter.split_documents(documents)


if __name__ == "__main__":
    from src.ingestion.load_documents import load_documents

    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} documents")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        print("=" * 60)
        print("Chunk:", chunk.page_content)
        print("Metadata:", chunk.metadata)
        print("-" * 60)
