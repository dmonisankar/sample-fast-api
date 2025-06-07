from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from app.config import OPENAI_API_KEY

# Initialize LangChain Chat Model
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

model = "gpt-3.5-turbo"
llm_config = {
    "model": model,
    "temperature": 0.4,
    "api_key": OPENAI_API_KEY,
}
llm = ChatOpenAI(model=model, openai_api_key=OPENAI_API_KEY)


async def get_llm_response(prompt: str) -> str:
    """Calls OpenAI API using LangChain and returns a response."""
    try:
        response = llm([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"


async def ai_response_stream(prompt: str):
    """Calls OpenAI API using LangChain and streams the response."""
    try:
        async for chunk in llm.astream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content  # Yield response chunks as they arrive
                # time.sleep(1)
    except Exception as e:
        yield f"Error: {str(e)}"
