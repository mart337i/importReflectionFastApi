from fastapi import APIRouter

router = APIRouter()

@router.get("/route2")
async def route2():
    return {"message": "Hello from route2"}