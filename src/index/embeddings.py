from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    """Obtiene la representación vectorial de un texto.

    Args:
        text (str): El texto a representar.

    Returns:
        list: La representación vectorial del texto.
    """
    embedding = model.encode(text)
    return embedding.tolist()


