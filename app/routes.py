from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import collection
from app.schemas import AgentSchema, UpdateAgentSchema, LLMRequest, LLMRequestWithMemory
from app.models import AgentDB
from app.services.llm_service import get_llm_response, ai_response_stream
from app.services.agentic_calculation import get_calculation
from app.services.langraph_agentic_calculation import get_langraph_calculation
from app.services.langraph_agentic_calculation_enhanced import (
    get_langraph_calculation_with_memory,
)
from app.services.llm_watsonx import get_info_watsonx
from app.services.langraph_agent_researcher import get_research_results
from fastapi.responses import StreamingResponse
from app.config import PHOENIX_ENDPOINT
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor


router = APIRouter()


# configure the Phoenix tracer
tracer_provider = register(
    project_name="md-llm-app",  # Default is 'default'
    auto_instrument=True,  # See 'Trace all calls made to a library' below
    endpoint=PHOENIX_ENDPOINT,
)
tracer = tracer_provider.get_tracer(__name__)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


# Create an agent
@router.post("/agents/", response_model=AgentDB)
async def create_agent(agent: AgentSchema):
    existing_agent = await collection.find_one({"name": agent.name})
    if existing_agent:
        raise HTTPException(status_code=400, detail="Agent already exists")

    agent_dict = agent.model_dump()
    result = await collection.insert_one(agent_dict)
    return AgentDB(id=str(result.inserted_id), **agent_dict)


# Read all agents
@router.get("/agents/", response_model=list[AgentDB])
async def get_users():
    agents = await collection.find().to_list(100)
    return [AgentDB(id=str(agent["_id"]), **agent) for agent in agents]


# Read a single user
@router.get("/agents/{agent_id}", response_model=AgentDB)
async def get_user(agent_id: str):
    agent = await collection.find_one({"_id": ObjectId(agent_id)})
    if not agent:
        raise HTTPException(status_code=404, detail="User not found")
    return AgentDB(id=str(agent["_id"]), **agent)


# Update agent
@router.put("/agents/{agent_id}", response_model=AgentDB)
async def update_agent(agent_id: str, update_data: UpdateAgentSchema):
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No valid fields provided")

    updated_agent = await collection.find_one_and_update(
        {"_id": ObjectId(agent_id)}, {"$set": update_dict}, return_document=True
    )

    if not updated_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return AgentDB(id=str(updated_agent["_id"]), **updated_agent)


# Delete agent
@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    result = await collection.delete_one({"_id": ObjectId(agent_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}


@router.post("/llm/")
async def ask_llm(request: LLMRequest):
    """Takes user input (prompt) and returns an AI-generated response."""
    response = await get_llm_response(request.prompt)

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {"prompt": request.prompt, "response": response}


@router.post("/calculate/")
async def caculate(request: LLMRequest):
    """Takes user input (prompt) and returns an AI-generated response."""

    response = await get_calculation(request.prompt)

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {"prompt": request.prompt, "response": response}


@router.post("/langraph_calculate/")
async def ask_langraph_llm(request: LLMRequest):
    """Takes user input (prompt) and returns an AI-generated response."""
    print(request.prompt)
    response = await get_langraph_calculation(request.prompt)

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {"prompt": request.prompt, "response": response}


@router.post("/langraph_calculate_enhanced/")
async def ask_langraph_llm_with_memory(request: LLMRequestWithMemory):
    """Takes user input (prompt) and returns an AI-generated response."""
    print(request.prompt)
    response, conversation_id = await get_langraph_calculation_with_memory(
        request.prompt, request.conversation_id
    )

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {
        "prompt": request.prompt,
        "response": response,
        "conversation_id": conversation_id,
    }


@router.post("/ask_watson/")
async def ask_watson(request: LLMRequest):
    """Takes user input (prompt) and returns an AI-generated response."""

    response = await get_info_watsonx(request.prompt)

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {"prompt": request.prompt, "response": response}


@router.post("/stream")
async def stream(request: LLMRequest):
    return StreamingResponse(
        ai_response_stream(request.prompt),
        media_type="text/event-stream",
        headers={"Content-Type": "text/event-stream"},
    )


@router.post("/langraph_research/")
async def research_agent(request: LLMRequest):
    """Takes user input (prompt) and uses a research agent to find and summarize information."""
    response = await get_research_results(request.prompt)

    if "Error" in response:
        raise HTTPException(status_code=500, detail=response)

    return {"prompt": request.prompt, "response": response}
