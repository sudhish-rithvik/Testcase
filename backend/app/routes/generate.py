from fastapi import APIRouter
from app.services.gemini_service import generate_testcases_with_retry

router = APIRouter()

@router.post("/generate-testcases")
def generate_testcases():
    return generate_testcases_with_retry(
        "Generate test cases for login using email and password"
    )
