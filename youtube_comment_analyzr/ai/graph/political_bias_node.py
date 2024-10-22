from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from youtube_comment_analyzr.ai.graph.state import CommentGraphState
from youtube_comment_analyzr.ai.prompts.system_prompts import POLITICAL_BIAS_PROMPT


class PoliticalBias(BaseModel):
    summary: str = Field(description="정치적 성향 요약")
    key_observations: List[str] = Field(description="주요 관찰 사항")
    conclusion: str = Field(description="결론 및 추가 고려사항")


llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
structured_llm = llm.with_structured_output(PoliticalBias)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", POLITICAL_BIAS_PROMPT),
        ("human", "질문: {question}\n댓글: {comments}"),
    ]
)

chain_llm = prompt | structured_llm


def political_bias_node(state: CommentGraphState) -> dict:
    """
    주어진 상태(state)에서 질문과 댓글을 추출하고, 이를 기반으로 정치성향을 분석합니다.

    Args:
        state (CommentGraphState): 상태 정보를 포함하는 딕셔너리.

    Returns:
        dict: 분석된 정치성향 정보를 포함하는 딕셔너리.
    """
    question = state["question"]
    comments = state["comments"]

    # 댓글 텍스트만 추출
    comment_texts = [comment["text"] for comment in comments]

    result = chain_llm.invoke(
        {"question": question, "comments": "\n".join(comment_texts)}
    )

    if not isinstance(result, PoliticalBias):
        raise ValueError("Invalid response type")

    return {**state, "political_bias": result}
