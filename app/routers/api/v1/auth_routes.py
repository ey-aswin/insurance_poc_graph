from fastapi import APIRouter, HTTPException
# from app.controllers.auth_controller import auth_controller

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Single sign-on Google SSO endpoint
@router.post("/google-sso")
def google_sso(token: str):
    # Placeholder for Google SSO logic
    # resp = auth_controller.google_sso(token)
    return {"message": "Google SSO successful", "token": token}

