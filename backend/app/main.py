import os
print("GEMINI_API_KEY loaded:", "GEMINI_API_KEY" in os.environ)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.generate import router as generate_router
from app.routes.upload import router as upload_router
from app.routes.download import router as download_router

app = FastAPI(title="TestCaseAI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router)
app.include_router(upload_router)
app.include_router(download_router)

@app.get("/")
def root():
    return {"status": "TestCaseAI backend running"}
