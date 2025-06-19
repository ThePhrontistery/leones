"""Logout endpoint for user session termination."""
from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/logout", response_class=RedirectResponse, include_in_schema=False)
async def logout(response: Response):
    """Clears the user cookie and redirects to login."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user")
    return response
