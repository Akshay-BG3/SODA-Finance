from fastapi import APIRouter

router = APIRouter(
    prefix="/ai-summary",
    tags=["AI Summary"]
)

@router.get("/")
def summary_status():
    return {"message": "AI Summary module is live"}
