from fastapi import APIRouter

router = APIRouter(
    prefix="/risk",
    tags=["risk detection"]
)

@router.get("/")
def summary_status():
    return {"message": "AI Summary module is live"}
