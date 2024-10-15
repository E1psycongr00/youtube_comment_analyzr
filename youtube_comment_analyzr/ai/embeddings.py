from enum import Enum

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel(Enum):
    JHGAN = "jhgan/ko-sroberta-multitask"
    INTFLOAT_LARGE = "intfloat/multilingual-e5-large-instruct"
    INTFLOAT_BASE = "intfloat/multilingual-e5-base"
    INTFLOAT_SMALL = "intfloat/multilingual-e5-small"
    BAAI = "BAAI/bge-m3"


def load_embeddings(model_name: EmbeddingModel, cache_folder: str):
    return HuggingFaceEmbeddings(model_name=model_name.value, cache_folder=cache_folder)


if __name__ == "__main__":
    embeddings = load_embeddings(EmbeddingModel.JHGAN, "models")
    print(embeddings)
