from fastapi import APIRouter

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.get("/")
def summary_status():
    return {"message": "AI Summary module is live"}
