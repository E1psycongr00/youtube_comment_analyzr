import re
from typing import Any, Dict, List, Type

from googleapiclient.discovery import build
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class YouTubeCommentToolInput(BaseModel):
    query: str = Field(..., description="YouTube 비디오 URL 또는 ID")
    max_results: int = Field(100, description="가져올 댓글의 최대 수")


class YouTubeCommentTool(BaseTool):
    """
    YouTubeCommentTool 클래스는 YouTube API를 사용하여 특정 비디오의 댓글을 가져오는 기능을 제공합니다.
    이 클래스는 YouTube API 키를 초기화하고, 비디오 ID 또는 URL을 통해 댓글을 가져올 수 있습니다.
    """

    name: str = "YouTube Comment Tool"
    description: str = "YouTube 비디오의 댓글을 가져오는 도구입니다. 비디오 URL 또는 ID를 입력으로 받습니다."
    args_schema: Type[BaseModel] = YouTubeCommentToolInput
    youtube: Any = None

    def __init__(self, api_key: str):
        """
        YouTubeCommentTool 클래스의 생성자입니다.
        YouTube API 키를 초기화합니다.

        :param api_key: YouTube API 키
        :raises ValueError: YouTube API 키가 제공되지 않았을 경우
        """
        super().__init__()
        if not api_key:
            raise ValueError("YouTube API 키가 제공되지 않았습니다.")
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def _run(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        특정 비디오의 댓글을 가져옵니다.

        :param query: 비디오 URL 또는 ID
        :param max_results: 가져올 댓글의 최대 수 (기본값: 100)
        :return: 댓글 목록 (리스트 형식)
        """
        video_id = self.extract_video_id(query)
        return self.get_video_comments(video_id, max_results)

    def get_video_comments(
        self, video_id: str, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        특정 비디오의 댓글을 가져옵니다.

        :param video_id: 댓글을 가져올 비디오의 ID
        :param max_results: 가져올 댓글의 최대 수 (기본값: 100)
        :return: 댓글 목록 (리스트 형식)
        """
        comments = []
        next_page_token = None

        while len(comments) < max_results:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results - len(comments)),
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(
                    {
                        "author": comment["authorDisplayName"],
                        "text": comment["textDisplay"],
                        "likes": comment["likeCount"],
                        "published_at": comment["publishedAt"],
                    }
                )

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return comments[:max_results]

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        YouTube URL에서 비디오 ID를 추출합니다.

        :param url: YouTube 비디오 URL 또는 ID
        :return: 추출된 비디오 ID
        :raises ValueError: 유효하지 않은 YouTube URL일 경우
        """
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
            r"(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})",
            r"(?:watch\?v=)([0-9A-Za-z_-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # URL 패턴이 일치하지 않으면 입력이 이미 비디오 ID인지 확인
        if re.match(r"^[0-9A-Za-z_-]{11}$", url):
            return url

        raise ValueError("유효하지 않은 YouTube URL 또는 비디오 ID입니다.")
