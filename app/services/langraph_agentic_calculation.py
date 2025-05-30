from app.services.tools.calculation_tools import (
    add_numbers,
    multiply_numbers,
    divide_number,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from app.config import PAYI_API_KEY

tools = [add_numbers, multiply_numbers, divide_number]
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125"
)

# For this ipynb we set parallel tool calling to false as math generally is done sequentially, and this time we have 3 tools that can do math
# the OpenAI model specifically defaults to parallel tool calling for efficiency, see https://python.langchain.com/docs/how_to/tool_calling_parallel/
# play around with it and see how the model behaves with math equations!
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


# System message
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)


# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()


async def get_langraph_calculation(prompt: str) -> str:
    """use langraph agents to calculate."""
    try:
        messages = [HumanMessage(content=prompt)]
        messages = react_graph.invoke({"messages": messages})
        last_message = messages["messages"][-1]
        return last_message.pretty_repr()

    except Exception as e:
        return f"Error: {str(e)}"
