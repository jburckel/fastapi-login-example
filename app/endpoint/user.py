from fastapi import Depends, APIRouter

from app import auth

router = APIRouter()


@router.post('/me/')
def get_my_info(
        current_user: auth.UserModelType = Depends(auth.get_current_user)
        ):
    return {'email': current_user.email, 'status': 'logged'}
