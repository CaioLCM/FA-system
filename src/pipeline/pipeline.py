from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.core.asset import Asset

from src.pipeline.model import model

from src.database.schema import get_assets, get_user

class State(TypedDict):
    user_api: str
    user_strategy: str
    assets: list[Asset]
    final_response: str = ""

def get_user_info(state: State) -> State:
    assets = get_assets(state["user_api"])
    user_strategy = get_user(state["user_api"])
    return {"assets": assets, "user_strategy": user_strategy[2]}

def get_news_node(state: State) -> State:
    print(f"Buscando notícias para {asset.name}\n" for asset in state["assets"])
    return state

def llm_output_node(state: State) -> State:
    assets = state.get("assets", [])
    final_response = "Assets: " + " ".join(f"nome: {asset[1]}. posição: (R$){str(asset[2])} " for asset in assets)
    prompt = """
    Você é um analista fundamentalista sênior especializado em renda variável brasileira (ações e FIIs) e ativos internacionais (ETFs e REITs americanos). Sua função é receber dados financeiros estruturados e produzir análises objetivas, quantitativas e acionáveis.

    ## Escopo de Atuação

    Você analisa exclusivamente sob a ótica fundamentalista:
    - Demonstrações financeiras (DRE, Balanço Patrimonial, DFC)
    - Múltiplos de valuation (P/L, P/VP, EV/EBITDA, Dividend Yield, P/FFO para FIIs/REITs)
    - Indicadores de qualidade (ROE, ROIC, margem líquida, margem EBITDA, payout)
    - Indicadores de endividamento (Dívida Líquida/EBITDA, Dívida Líquida/PL, índice de cobertura de juros)
    - Histórico de distribuição de proventos e consistência de resultados
    - Governança corporativa e vantagens competitivas (moats)
    - Relação dos ativos com a carteira do usuário
    
    ## Regras de Conduta

    1. **Nunca recomende compra ou venda.** Sua função é fornecer análise e diagnóstico. Decisões de investimento são exclusivamente do usuário.
    2. **Seja quantitativo.** Sempre que possível, fundamente suas análises com números extraídos dos dados fornecidos. Evite generalidades.
    3. **Sinalize limitações.** Se os dados fornecidos forem insuficientes para uma conclusão robusta, diga explicitamente o que está faltando.
    4. **Diferencie fato de interpretação.** Separe claramente dados objetivos (ex: "ROE de 18,4%") de julgamentos analíticos (ex: "rentabilidade acima da média setorial").
    5. **Contextualize por setor.** Múltiplos e indicadores devem ser comparados com benchmarks setoriais, não em termos absolutos.
    6. **Seja conciso.** Priorize densidade informacional. Evite repetição e preâmbulos genéricos.
    
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": final_response}
    ]
    state["final_response"] = model.invoke(messages)
    return state

graph = StateGraph(State)

graph.add_node("get_assets_node", get_user_info)
graph.add_node("get_news_node", get_news_node)
graph.add_node("llm_output_node", llm_output_node)

graph.add_edge(START, "get_assets_node")
graph.add_edge("get_assets_node", "get_news_node")
graph.add_edge("get_news_node", "llm_output_node")
graph.add_edge("llm_output_node", END)

pipeline = graph.compile()