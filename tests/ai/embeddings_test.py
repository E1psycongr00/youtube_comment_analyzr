import unittest
from unittest.mock import MagicMock, patch

from youtube_comment_analyzr.ai.embeddings import EmbeddingModel, load_embeddings


class TestEmbeddings(unittest.TestCase):
    @patch("youtube_comment_analyzr.ai.embeddings.HuggingFaceEmbeddings")
    def test_load_embeddings(self, mock_hf_embeddings):
        # 모의 HuggingFaceEmbeddings 객체 설정
        mock_embeddings = MagicMock()
        mock_hf_embeddings.return_value = mock_embeddings

        # 함수 호출
        result = load_embeddings(EmbeddingModel.JHGAN, "test_cache")

        # assertions
        mock_hf_embeddings.assert_called_once_with(
            model_name="jhgan/ko-sroberta-multitask", cache_folder="test_cache"
        )
        self.assertEqual(result, mock_embeddings)

    def test_embedding_model_enum(self):
        # EmbeddingModel enum의 값들을 테스트
        self.assertEqual(EmbeddingModel.JHGAN.value, "jhgan/ko-sroberta-multitask")
        self.assertEqual(
            EmbeddingModel.INTFLOAT_LARGE.value,
            "intfloat/multilingual-e5-large-instruct",
        )
        self.assertEqual(
            EmbeddingModel.INTFLOAT_BASE.value, "intfloat/multilingual-e5-base"
        )
        self.assertEqual(
            EmbeddingModel.INTFLOAT_SMALL.value, "intfloat/multilingual-e5-small"
        )
        self.assertEqual(EmbeddingModel.BAAI.value, "BAAI/bge-m3")


if __name__ == "__main__":
    unittest.main()
