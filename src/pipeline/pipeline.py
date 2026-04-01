from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.core.asset import Asset

from src.pipeline.model import model

class State(TypedDict):
    assets: list[Asset]
    final_response: str = ""

def get_news_node(state: State) -> State:
    print("Node 2")
    return state

def llm_output_node(state: State) -> State:
    assets = state.get("assets", [])
    final_response = "Assets: " + " ".join(f"nome: {asset.name}. posição: {asset.position} " for asset in assets)
    messages = [
        {"role": "system", "content": "Você é um mano da quebrada analisando os ativos de uma pessoa, traga uma resposta comica a respeito da carteira dessa pessoa"},
        {"role": "user", "content": final_response}
    ]
    state["final_response"] = model.invoke(messages)
    return state

graph = StateGraph(State)

graph.add_node("get_news_node", get_news_node)
graph.add_node("llm_output_node", llm_output_node)

graph.add_edge(START, "get_news_node")
graph.add_edge("get_news_node", "llm_output_node")
graph.add_edge("llm_output_node", END)

pipeline = graph.compile()