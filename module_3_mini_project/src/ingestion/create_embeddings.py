from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "The maximum fine for a violation is $1,000.",
    "Residents may be fined up to one thousand dollars.",
    "Community meetings are held annually.",
]

embedding = model.encode(texts)

print(type(embedding))
print(len(embedding))
print(embedding)
print(embedding.shape)