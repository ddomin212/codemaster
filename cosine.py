import jellyfish
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example code snippets
code_snippet1 = "def add(a, b): return a + b"
code_snippet2 = "def sum(a, b): return a + b"
code_snippet3 = "def multiply(x, y): return x * y"

# Tokenize and vectorize the code snippets for cosine similarity
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([code_snippet1, code_snippet2, code_snippet3])

# Compute cosine similarity between code snippets
cosine_similarity_matrix = cosine_similarity(X)

# Jaro similarity threshold
jaro_threshold = 0.8

# Cosine similarity threshold
cosine_threshold = 0.8

# Identify duplicates based on Jaro similarity
if jellyfish.jaro_similarity(code_snippet1, code_snippet2) >= jaro_threshold:
    print("Jaro similarity: Code snippet 1 is similar to code snippet 2")

# Identify duplicates based on cosine similarity
for i in range(len(cosine_similarity_matrix)):
    for j in range(i + 1, len(cosine_similarity_matrix)):
        if cosine_similarity_matrix[i][j] >= cosine_threshold:
            print(
                f"Cosine similarity: Code snippet {i+1} is similar to code snippet {j+1}"
            )
