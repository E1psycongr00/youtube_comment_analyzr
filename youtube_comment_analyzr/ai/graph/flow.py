from langgraph.graph import END, START, StateGraph

from youtube_comment_analyzr.ai.graph.classifier_node import classfier_node
from youtube_comment_analyzr.ai.graph.extract_comment import extract_comment_node
from youtube_comment_analyzr.ai.graph.generate_node import generate_node
from youtube_comment_analyzr.ai.graph.political_bias_node import political_bias_node
from youtube_comment_analyzr.ai.graph.search_bad_user_node import search_bad_user_node
from youtube_comment_analyzr.ai.graph.state import CommentGraphState


def decide_by_keyword(state: CommentGraphState) -> str:
    print("판단중......")
    if state["keyword"] == "악성댓글유저":
        return "bad_comment_user"
    if state["keyword"] == "정치성향":
        return "political_bias"
    if state["youtube_url_or_id"]:
        return "extract_comment"
    return "cannot_solve"


def decide_by_url_or_id_exist(state: CommentGraphState):
    if state["youtube_url_or_id"]:
        return "extract_comment"
    return "cannot_solve"


def cannot_solve_question_node(state: CommentGraphState):
    if state["keyword"] == "None":
        return {"generation": "I cannot solve this question."}
    if not state["youtube_url_or_id"]:
        return {"generation": "plz provide youtube url or id"}
    return {"generation": "I cannot solve this question."}


def compile_graph():
    _graph = StateGraph(CommentGraphState)
    _graph.add_node("QuestionClassifierNode", classfier_node)
    _graph.add_node("ExtractCommentNode", extract_comment_node)
    _graph.add_node("SearchBadUserNode", search_bad_user_node)
    _graph.add_node("PoliticalBiasNode", political_bias_node)
    _graph.add_node("GenerateNode", generate_node)
    _graph.add_node("CannotSolveQuestionNode", cannot_solve_question_node)

    _graph.add_edge(START, "QuestionClassifierNode")
    _graph.add_conditional_edges(
        "QuestionClassifierNode",
        decide_by_url_or_id_exist,
        {
            "cannot_solve": "CannotSolveQuestionNode",
            "extract_comment": "ExtractCommentNode",
        },
    )
    _graph.add_conditional_edges(
        "ExtractCommentNode",
        decide_by_keyword,
        {
            "cannot_solve": "CannotSolveQuestionNode",
            "bad_comment_user": "SearchBadUserNode",
            "political_bias": "PoliticalBiasNode",
        },
    )
    _graph.add_edge("CannotSolveQuestionNode", END)
    _graph.add_edge("SearchBadUserNode", "GenerateNode")
    _graph.add_edge("PoliticalBiasNode", "GenerateNode")
    _graph.add_edge("GenerateNode", END)

    return _graph.compile()
