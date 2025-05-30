# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.tools import tool
# from langgraph.graph import MessagesState, StateGraph, START
# from langgraph.prebuilt import tools_condition, ToolNode
# import os
# from langchain_core.prompts import PromptTemplate
# from tavily import TavilyClient
# from dotenv import load_dotenv
# from app.config import PAYI_API_KEY

# # Load environment variables
# load_dotenv()

# # Initialize Tavily client with API key from environment
# # For production, add TAVILY_API_KEY to your .env file
# tavily_api_key = os.getenv("TAVILY_API_KEY")
# tavily_client = TavilyClient(api_key=tavily_api_key)


# # Define research tools
# @tool
# def search_web(query: str) -> str:
#     """Search the web for information about a topic using Tavily Search API."""
#     try:
#         # Use Tavily API for web search
#         search_result = tavily_client.search(
#             query=query,
#             search_depth="advanced",
#             include_domains=None,
#             exclude_domains=None,
#             include_answer=True,
#             max_results=5,
#         )

#         # Format the search results
#         formatted_results = f"Search results for '{query}':\n\n"

#         if search_result.get("answer"):
#             formatted_results += f"Answer: {search_result.get('answer')}\n\n"

#         formatted_results += "Sources:\n"
#         for idx, result in enumerate(search_result.get("results", []), 1):
#             formatted_results += f"{idx}. {result.get('title', 'No title')}\n"
#             formatted_results += f"   URL: {result.get('url', 'No URL')}\n"
#             formatted_results += (
#                 f"   Content: {result.get('content', 'No content')[:200]}...\n\n"
#             )

#         return formatted_results

#     except Exception as e:
#         # Fallback to mock data if API fails or isn't configured
#         return f"Search failed or API key not configured. Error: {str(e)}\n\nFallback mock results for '{query}': This would connect to a search engine in production."


# @tool
# def summarize_information(text: str) -> str:
#     """Summarize a large body of text into key points using LLM."""
#     try:
#         # Define summarization prompt
#         summarization_prompt = PromptTemplate.from_template(
#             """You are an expert summarizer. Your task is to create a concise summary of the following text.
#             Extract key points, main ideas, and important details.
            
#             TEXT TO SUMMARIZE:
#             {text}
            
#             SUMMARY:"""
#         )

#         # Use the LLM to generate the summary
#         summarization_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

#         # Format the prompt with the input text
#         formatted_prompt = summarization_prompt.format(text=text)

#         # Get the summary from the LLM
#         summary_message = summarization_llm.invoke(
#             [HumanMessage(content=formatted_prompt)]
#         )

#         return summary_message.content

#     except Exception as e:
#         # Fallback if summarization fails
#         return f"Summarization failed. Error: {str(e)}\n\nFallback: This would be a summary of the provided information."


# # Set up LLM

# llm = ChatOpenAI(
#     model="gpt-3.5-turbo-0125", default_headers={"xProxy-api-key": PAYI_API_KEY}
# )

# # Configure tools
# tools = [search_web, summarize_information]
# llm_with_tools = llm.bind_tools(tools)

# # System message
# sys_msg = SystemMessage(
#     content="""You are a research assistant capable of finding information and summarizing it effectively.
#     You can search for information on topics and provide concise summaries.
#     When asked a question, you should:
#     1. Determine what information is needed
#     2. Search for that information using the search_web tool
#     3. If the search results are lengthy, use the summarize_information tool to create a concise summary
#     4. Present a well-organized, coherent response that directly answers the user's query
    
#     Always cite your sources when providing information.
#     """
# )


# # Define the assistant node
# def assistant(state: MessagesState):
#     """Process the current state and respond using the LLM with tools."""
#     messages = [sys_msg] + state["messages"]
#     response = llm_with_tools.invoke(messages)
#     return {"messages": [response]}


# # Create the graph
# def create_research_graph():
#     """Create and return the research agent graph."""
#     builder = StateGraph(MessagesState)

#     # Add nodes
#     builder.add_node("assistant", assistant)
#     builder.add_node("tools", ToolNode(tools))

#     # Add edges
#     builder.add_edge(START, "assistant")
#     builder.add_conditional_edges(
#         "assistant",
#         tools_condition,
#     )
#     builder.add_edge("tools", "assistant")

#     return builder.compile()


# # Create the graph once
# research_graph = create_research_graph()


async def get_research_results(prompt: str) -> str:
    """Use LangGraph research agent to find and summarize information."""
    return ""
#     try:
#         messages = [HumanMessage(content=prompt)]
#         result = research_graph.invoke({"messages": messages})
#         last_message = result["messages"][-1]
#         return last_message.pretty_repr()
#     except Exception as e:
#         return f"Error: {str(e)}"
