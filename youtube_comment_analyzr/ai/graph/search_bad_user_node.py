from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from youtube_comment_analyzr.ai.graph.state import CommentGraphState
from youtube_comment_analyzr.ai.prompts.system_prompts import SEARCH_BAD_USER_PROMPT


class BadUserInfo(BaseModel):
    bad_user_id: str = Field(description="The bad user id")
    bad_rate: float = Field(description="The bad rate 1 ~ 5")
    reason: str = Field(description="The reason of bad rate")


class SearchBadUserOutput(BaseModel):
    bad_users: List[BadUserInfo] = Field(description="The bad users info list")


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
structured_llm = llm.with_structured_output(SearchBadUserOutput)

human_prompt = """질문: {question}
댓글 목록: {comments}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SEARCH_BAD_USER_PROMPT),
        ("human", human_prompt),
    ]
)

chain_llm = prompt | structured_llm


def search_bad_user_node(state: CommentGraphState):
    question = state["question"]
    comments = state["comments"]
    response = chain_llm.invoke({"question": question, "comments": comments})
    if not isinstance(response, SearchBadUserOutput):
        raise ValueError("Invalid response type")
    return {**state, "bad_users": response.bad_users}

