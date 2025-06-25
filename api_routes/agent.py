from fastapi import APIRouter

router = APIRouter(
    prefix="/agent",
    tags=["Agent Layer"]
)

@router.get("/")
def summary_status():
    return {"message": "AI Summary module is live"}
