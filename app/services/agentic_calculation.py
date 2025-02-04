import openai
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from autogen import ConversableAgent
from typing import Annotated
from app.services.tools.calculation_tools import add_numbers, multiply_numbers

import asyncio
from autogen import (
    AssistantAgent,
    UserProxyAgent,
    GroupChat,
    GroupChatManager,
    config_list_from_json,
)
from langchain.utilities import WikipediaAPIWrapper  # For Wikipedia tool
from langchain.agents import Tool


from app.config import OPENAI_API_KEY

model = "gpt-3.5-turbo"
llm_config = {
    "model": model,
    "temperature": 0.4,
    "api_key": OPENAI_API_KEY,
}

async def get_calculation(prompt: str) -> str:
    """use autogen agents to calculate."""
    try:
        # Define the assistant agent that suggests tool calls.
        assistant = ConversableAgent(
            name="CalculatorAssistant",
            system_message="You are a helpful AI calculator. Return 'TERMINATE' when the task is done.",
            llm_config=llm_config,
        )

        # The user proxy agent is used for interacting with the assistant agent and executes tool calls.
        user_proxy = ConversableAgent(
            name="User",
            is_termination_msg=lambda msg: msg.get("content") is not None
            and "TERMINATE" in msg["content"],
            human_input_mode="NEVER",
        )

        # Register the tool signatures with the assistant agent.
        assistant.register_for_llm(name="add_numbers", description="Add two numbers")(
            add_numbers
        )
        assistant.register_for_llm(name="multiply_numbers", description="Multiply two numbers")(
            multiply_numbers
        )

        # Register the tool functions with the user proxy agent.
        user_proxy.register_for_execution(name="add_numbers")(add_numbers)
        user_proxy.register_for_execution(name="multiply_numbers")(multiply_numbers)

        chat_result = user_proxy.initiate_chat(assistant, message=prompt, summary_method='reflection_with_llm')
        return chat_result.summary

    except Exception as e:
        return f"Error: {str(e)}"

