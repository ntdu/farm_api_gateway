from fastapi import APIRouter, Depends, Request, Response, status

router = APIRouter(prefix="/crop-health-service", tags=["crop-health-service"])


@router.get('/gdhgf', status_code=status.HTTP_200_OK)
async def get_users(request: Request, response: Response):
    
    return 'users'

