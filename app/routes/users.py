from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
async def register_user() -> dict:
    """Register user in blog"""
    return {"message": "register_user()"}


@router.post("/login")
async def login_user() -> dict:
    """Login user in blog"""
    return {"message": "login_user()"}


@router.get("/{user_id}")
async def get_user(user_id: int) -> dict:
    """Get user in blog by id"""
    return {"message": f"get_user({user_id})"}


@router.put("/{user_id}")
async def update_user(user_id: int) -> dict:
    """Update user in blog by id"""
    return {"message": f"update_user({user_id})"}
