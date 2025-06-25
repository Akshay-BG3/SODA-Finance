from fastapi import APIRouter

router = APIRouter(
    prefix="/statement",
    tags=["Statement Analyzer"]
)

@router.get("/")
def summary_status():
    return {"message": "AI Summary module is live"}
