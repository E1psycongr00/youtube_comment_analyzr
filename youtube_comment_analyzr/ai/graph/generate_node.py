from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI

from youtube_comment_analyzr.ai.graph.state import CommentGraphState
from youtube_comment_analyzr.ai.prompts.system_prompts import GENERATE_PROMPT

human_prompt = """ 질문: {question}
악성 유저 정보: {bad_users}
관련 문서: {documents}
"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", GENERATE_PROMPT),
        ("human", human_prompt),
    ]
)

chain_llm = prompt | llm | StrOutputParser()


def generate_node(state: CommentGraphState):
    # 각 키에 대해 안전하게 값을 가져오고, 없으면 기본값 사용
    question = state.get("question", "")
    bad_users = state.get("bad_users", "")
    documents = state.get("documents", "")

    # chain_llm.invoke()에 안전하게 처리된 값들을 전달
    response = chain_llm.invoke(
        {"question": question, "bad_users": bad_users, "documents": documents}
    )

    # 원래 상태와 새로운 'generation' 키를 병합하여 반환
    return {**state, "generation": response}
