from typing import List, TypedDict


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
    """
    question: str
    generation: str
    keyword: str
    youtube_url_or_id: str
    web_search: str
    documents: List[str]
    comments: List[str]