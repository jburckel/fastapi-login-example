from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app import auth, crud, database, exception, schema

router = APIRouter()


@router.get('/form/', response_class=HTMLResponse)
async def login_form():
    return """
    <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            <h1>Please register!</h1>
            <form action='/register/form/token/' method='post'>
                <input type='email' name='username' />
                <input type='password' name='password' />
                <input type='submit' />
            </form>
            <a href='/register/google/'>Google</a>
            <a href='/register/facebook/'>Facebook</a>
        </body>
    </html>
    """


@router.post('/form/token/', response_model=schema.token.Token)
def create_user_from_form(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    try:
        new_user = schema.user.RegisterLocal(username=username, password=password)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=jsonable_encoder(err.errors()))
    user = crud.user.register(db, data=new_user)
    return auth.get_access_token(user.id)


@router.post('/token/', response_model=schema.token.Token)
def create_user(
    new_user: schema.user.RegisterLocal,
    db: Session = Depends(database.get_db)
):
    user = crud.user.register(db, data=new_user)
    return auth.get_access_token(user.id)


@router.get('/{provider}/')
def register_provider_redirect(
    provider: str,
    request: Request
):

    oauth2_provider = auth.get_oauth2_provider(provider)
    request_uri = oauth2_provider.get_redirect_url(
        callback_url=str(request.url) + 'callback/'
    )
    return RedirectResponse(request_uri)


@router.get('/{provider}/callback/', response_model=schema.token.Token)
def register_provider_callback(
    provider: str,
    code: str,
    request: Request,
    db: Session = Depends(database.get_db)
):

    oauth2_provider = auth.get_oauth2_provider(provider)
    userinfo = oauth2_provider.get_user_info(request_url=str(request.url), code=code)

    email = userinfo.get('email')
    sub = userinfo.get('sub')
    if sub is None:
        sub = userinfo.get('id')

    if userinfo.get('email_verified') is False or email is None or sub is None:
        raise exception.wrong_credential

    new_user = schema.user.RegisterProvider(
        email=email,
        sub=sub,
        provider=provider
    )

    user = crud.user.register(
        db,
        data=new_user
    )

    return auth.get_access_token(user.id)
