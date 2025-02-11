from langchain_ibm import ChatWatsonx
from langgraph.prebuilt import create_react_agent

from langchain_core.messages import HumanMessage

from app.config import WATSONX_APIKEY
from app.config import WATSONX_PROJECT_ID
from app.config import WATSONX_URL

from app.services.tools.prebuilt_tools import youtube_search, weather_search

llm = ChatWatsonx(
    model_id="ibm/granite-3-8b-instruct",
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


tools = [weather_search, youtube_search]
llm_with_tools = llm.bind_tools(tools)

agent_executor = create_react_agent(llm, tools)


async def get_info_watsonx(prompt: str) -> str:
    """use agent backed by watsonx model to respond."""
    try:
        messages = [HumanMessage(content=prompt)]

        response = agent_executor.invoke({"messages": messages})
        last_message = response["messages"][-1]
        return last_message.pretty_repr()

    except Exception as e:
        return f"Error: {str(e)}"
