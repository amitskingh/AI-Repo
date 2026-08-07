import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4")

text = "I love python!"


tokens = encoding.encode(text)
print(f"Tokens: {tokens}")
print(f"Number of tokens: {len(tokens)}")
