from typing import Any, List, TypedDict

from youtube_comment_analyzr.youtube.comment_tool import YouTubeComment


class CommentGraphState(TypedDict):
    """
    The state of the comment graph.

    Attributes:
        question: question.
        generation: generate answer.
        keyword: keyword by classifier LLM.
        youtube_url_or_id: youtube url or id by classifier LLM.
        web_search: whether to add search.
        documents: list of documents.
        comments: list of comments.
        bad_users: list of bad users.
    """

    question: str
    generation: str
    keyword: str
    youtube_url_or_id: str
    web_search: str
    documents: List[str]
    comments: List[YouTubeComment]
    bad_users: List[Any]
