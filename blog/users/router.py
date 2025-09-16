from fastapi import APIRouter, status


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user():
    raise NotImplementedError()
