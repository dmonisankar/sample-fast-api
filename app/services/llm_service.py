import openai
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

import asyncio
from langchain.utilities import WikipediaAPIWrapper  # For Wikipedia tool
from langchain.agents import Tool


from app.config import OPENAI_API_KEY

# Initialize LangChain Chat Model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

model = "gpt-3.5-turbo"
llm_config = {
    "model": model,
    "temperature": 0.4,
    "api_key": OPENAI_API_KEY,
}


async def get_llm_response(prompt: str) -> str:
    """Calls OpenAI API using LangChain and returns a response."""
    try:
        response = llm([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"



