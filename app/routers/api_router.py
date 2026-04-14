from fastapi import APIRouter, HTTPException

from app.routers.api.v1.embedding_router import router as embedding_router_v1
from app.routers.api.v1.prompt_router import router as prompt_router_v1
from app.routers.api.v1.policy_routes import router as policy_router_v1
from app.utils.logger_utils import logger

router = APIRouter()

# Include sub-routers for different API versions and functionalities
router.include_router( router=embedding_router_v1)

router.include_router( router=prompt_router_v1)

router.include_router( router=policy_router_v1)