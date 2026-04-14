from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers.api_router import router as api_router

load_dotenv()  # Load environment variables from .env file



import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "Your API is healthy!"}

app.include_router(api_router)  # Include the main API router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True) 