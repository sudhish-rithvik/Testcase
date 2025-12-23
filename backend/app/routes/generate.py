from fastapi import APIRouter
from app.services.gemini_service import call_gemini

router = APIRouter()

@router.post("/generate-testcases")
def generate_testcases():
    return call_gemini(
        "Generate test cases for login using email and password"
    )
