from fastapi import APIRouter, HTTPException

from app.controllers.prompt_controller import prompt_controller
from app.utils.logger_utils import logger

router = APIRouter(prefix="/api/v1/prompt", tags=["prompt"])


@router.post("/generate")
def generate_prompt(query: str):
    # Placeholder for prompt generation logic
    logger.info("Generating prompt...")
    resp =prompt_controller.generate_prompt(query)
    return resp


@router.post("/extract-graph/{session_id}")
def extract_graph_from_embedding(session_id: str, query: str = "Which company is provoiding this insurance?"):
    logger.info("Extracting graph from embedding info...")
    graph_data = prompt_controller.prompt_on_graph_from_embedding(session_id=session_id, query=query)
    return graph_data