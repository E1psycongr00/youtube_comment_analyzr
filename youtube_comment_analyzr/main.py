import os
import sys

import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_comment_analyzr.ai.graph.flow import compile_graph

load_dotenv()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bad_users" not in st.session_state:
    st.session_state.bad_users = []
if "political_bias" not in st.session_state:
    st.session_state.political_bias = {}


# 메인 컨텐츠 영역
def main_content():
    st.title("YouTube 댓글 분석 챗봇")

    # 채팅 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요...")

    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                ai_response = process_input(user_input)
                st.markdown(ai_response)

        # AI 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # 사이드바 업데이트
        sidebar()


# 사이드바 (우측에 표시)
def sidebar():
    with st.sidebar:
        st.title("분석 정보")

        # 문제가 있는 사용자 표시
        if st.session_state.bad_users:
            st.markdown("### 문제가 있는 사용자")
            st.markdown("\n".join([f"- {user}" for user in st.session_state.bad_users]))

        # 정치적 편향 표시
        if st.session_state.political_bias:
            st.markdown("### 정치적 편향")
            if isinstance(st.session_state.political_bias, dict):
                for bias, value in st.session_state.political_bias.items():
                    st.markdown(f"- **{bias}**: {value}")
            else:
                political_bias = st.session_state.political_bias
                st.markdown("**요약**:")
                st.markdown(political_bias.summary)
                st.markdown("**주요 관찰**:")
                st.markdown(
                    "\n".join([f"- {obs}" for obs in political_bias.key_observations])
                )
                st.markdown("**결론**:")
                st.markdown(political_bias.conclusion)


# 사용자 입력 처리 및 응답 생성 함수
def process_input(user_input):
    # AI 그래프 컴파일
    app = compile_graph()

    # AI 응답 생성
    response = app.invoke({"question": user_input})

    # bad_users와 political_bias 업데이트
    st.session_state.bad_users = response.get("bad_users", [])
    st.session_state.political_bias = response.get("political_bias", {})

    return response.get(
        "generation", "죄송합니다. 응답을 생성하는 데 문제가 발생했습니다."
    )


# 메인 애플리케이션
def main():
    main_content()


if __name__ == "__main__":
    main()
