from typing import List

from youtube_comment_analyzr.ai.graph.state import CommentGraphState
from youtube_comment_analyzr.youtube.comment_tool import (
    YouTubeComment,
    YouTubeCommentTool,
)

comment_tool = YouTubeCommentTool()


def extract_comment_node(state: CommentGraphState):
    youtube_url_or_id = state["youtube_url_or_id"]
    if not youtube_url_or_id:
        return state

    comments: List[YouTubeComment] = comment_tool.invoke(
        {"query": youtube_url_or_id, "max_results": 100}
    )
    return {**state, "comments": comments}
