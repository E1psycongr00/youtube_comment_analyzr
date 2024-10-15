import unittest
from unittest.mock import patch

from youtube_comment_analyzr.youtube.comment_tool import (
    YouTubeCommentTool,
    YouTubeCommentToolInput,
)


class TestYouTubeCommentTool(unittest.TestCase):

    @patch('youtube_comment_analyzr.youtube.comment_tool.build')
    def setUp(self, mock_build):
        self.api_key = 'fake_api_key'
        self.tool = YouTubeCommentTool(self.api_key)
        self.mock_youtube = mock_build.return_value

    def test_init_with_missing_api_key(self):
        with self.assertRaises(ValueError):
            YouTubeCommentTool('')

    def test_extract_video_id(self):
        test_cases = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ]
        for url, expected_id in test_cases:
            self.assertEqual(self.tool.extract_video_id(url), expected_id)

    def test_extract_video_id_invalid_url(self):
        with self.assertRaises(ValueError):
            self.tool.extract_video_id("https://www.example.com")

    def test_get_video_comments(self):
        mock_response = {
            'items': [
                {
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'authorDisplayName': '테스트 사용자',
                                'textDisplay': '테스트 댓글입니다.',
                                'likeCount': 10,
                                'publishedAt': '2023-04-01T12:00:00Z'
                            }
                        }
                    }
                }
            ],
            'nextPageToken': None
        }

        self.mock_youtube.commentThreads().list().execute.return_value = mock_response

        comments = self.tool.get_video_comments('test_video_id', max_results=1)

        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]['author'], '테스트 사용자')
        self.assertEqual(comments[0]['text'], '테스트 댓글입니다.')
        self.assertEqual(comments[0]['likes'], 10)
        self.assertEqual(comments[0]['published_at'], '2023-04-01T12:00:00Z')

    def test_run(self):
        with patch.object(YouTubeCommentTool, 'get_video_comments') as mock_get_comments:
            mock_get_comments.return_value = [{'author': 'Test User', 'text': 'Test Comment'}]
            input_data = YouTubeCommentToolInput(
                query="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                max_results=100
            )
            result = self.tool._run(**input_data.dict())
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['author'], 'Test User')
            self.assertEqual(result[0]['text'], 'Test Comment')

    def test_args_schema(self):
        self.assertEqual(self.tool.args_schema, YouTubeCommentToolInput)

if __name__ == '__main__':
    unittest.main()
