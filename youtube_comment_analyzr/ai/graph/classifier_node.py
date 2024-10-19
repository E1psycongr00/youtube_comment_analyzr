from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from youtube_comment_analyzr.ai.graph.state import CommentGraphState
from youtube_comment_analyzr.ai.prompts.system_prompts import QUESTION_CLASSIFIER_PROMPT


class QuestionClassifierOutput(BaseModel):
    keyword: str = Field(
        description="The keyword in ['정치성향', '악성댓글유저', 'None']"
    )
    youtube_url_or_id: str = Field(description="The YouTube URL or ID")


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm = llm.with_structured_output(QuestionClassifierOutput)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", QUESTION_CLASSIFIER_PROMPT),
        ("human", "{question}"),
    ]
)

chain_llm = prompt | structured_llm


def classfier_node(state: CommentGraphState) -> dict:
    """
    주어진 상태(state)에서 질문을 추출하고, 이를 기반으로 키워드를 분류합니다.
    분류된 키워드와 원래 질문을 반환합니다.

    Args:
        state (CommentGraphState): 상태 정보를 포함하는 딕셔너리.

    Returns:
        dict: 분류된 키워드와 원래 질문을 포함하는 딕셔너리.

    Raises:
        ValueError: 반환된 결과가 QuestionClassifierOutput의 인스턴스가 아닌 경우.
    """
    question = state["question"]
    result = chain_llm.invoke({"question": question})
    print(result)

    if not isinstance(result, QuestionClassifierOutput):
        raise ValueError("Invalid result type")

    return {
        "keyword": result.keyword,
        "youtube_url_or_id": result.youtube_url_or_id,
        "question": question,
    }
