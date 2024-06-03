from fastapi import APIRouter

router = APIRouter()

@router.get("/route1")
async def route1():
    return {"message": "Hello from route1"}