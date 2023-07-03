from fastapi import APIRouter, Depends, Request, Response, status


from src.utils import route   
from .datastructures import (
    UsernamePasswordForm,
    UserForm,
    UserUpdateForm
)
from src.settings import settings

router = APIRouter(prefix="", tags=["auth-forward"])


@route(
    request_method=router.post,
    path='/api/login',
    status_code=status.HTTP_201_CREATED,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False,
    post_processing_func='src.utils.post_processing.access_token_generate_handler',
    response_model='src.routers.auth_forward.datastructures.users.LoginResponse'
)
async def login(
    username_password: UsernamePasswordForm,
    request: Request, response: Response
):
    pass
