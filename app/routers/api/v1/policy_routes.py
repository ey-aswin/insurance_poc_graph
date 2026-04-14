from fastapi import APIRouter, HTTPException
from app.utils.logger_utils import logger
from app.controllers.policy_controller import policy_controller

router = APIRouter(prefix="/api/v1/policy", tags=["policy"])

@router.get("/{policy_id}")
async def get_policy(policy_id: str):
    try:
        policy_data = policy_controller.get_policy_details(policy_id)
        return {"message": "Policy retrieved successfully!", "policy_data": policy_data}
    except Exception as e:
        logger.error(f"Error retrieving policy {policy_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
        