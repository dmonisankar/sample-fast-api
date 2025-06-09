from app.services.tools.calculation_tools import (
    add_numbers,
    multiply_numbers,
    divide_number,
)
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from langgraph.checkpoint.memory import MemorySaver

from app.utils import generate_unique_id

from langchain_ibm import ChatWatsonx

from app.config import WATSONX_APIKEY
from app.config import WATSONX_PROJECT_ID
from app.config import WATSONX_URL

tools = [add_numbers, multiply_numbers, divide_number]
# llm = ChatOpenAI(model="gpt-4o")
# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
# ibm/granite-3-8b-instruct  -- memory not working
llm = ChatWatsonx(
    model_id="mistralai/mistral-large",
    url=WATSONX_URL,
    apikey=WATSONX_APIKEY,
    project_id=WATSONX_PROJECT_ID,
    params={
        "decoding_method": "greedy",
        "temperature": 0,
        "min_new_tokens": 5,
        "max_new_tokens": 2000,
    },
)


# For this ipynb we set parallel tool calling to false as math generally is done sequentially, and this time we have 3 tools that can do math
# the OpenAI model specifically defaults to parallel tool calling for efficiency, see https://python.langchain.com/docs/how_to/tool_calling_parallel/
# play around with it and see how the model behaves with math equations!
# llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
llm_with_tools = llm.bind_tools(tools)


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
memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer=memory)
react_graph = builder.compile()


async def get_langraph_calculation_with_memory(
    prompt: str, conversation_id: str = None
) -> tuple[str, str]:
    """use langraph agents to calculate."""
    try:
        if not conversation_id:
            conversation_id = generate_unique_id()

        config = {"configurable": {"thread_id": conversation_id}}
        messages = [HumanMessage(content=prompt)]
        messages = react_graph_memory.invoke({"messages": messages}, config)
        last_message = messages["messages"][-1]
        return last_message.pretty_repr(), conversation_id

    except Exception as e:
        return f"Error: {str(e)}", (conversation_id or "unknown")
