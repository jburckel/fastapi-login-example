from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
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
            <title>Login</title>
        </head>
        <body>
            <h1>Please login!</h1>
            <form action='/login/token/' method='post'>
                <input type='email' name='username' />
                <input type='password' name='password' />
                <input type='submit' />
            </form>
            <a href='/login/google/'>Google</a>
            <a href='/login/facebook/'>Facebook</a>
        </body>
    </html>
    """


@router.post('/token/')
def login(
        db: Session = Depends(database.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
        ):

    user = crud.user.login(
        db,
        email=form_data.username,
        password=form_data.password
    )

    return auth.get_access_token(user.id)


@router.get('/{provider}/')
def oauth2_provider_redirect(
    provider: str,
    request: Request
):

    oauth2_provider = auth.get_oauth2_provider(provider)

    redirect_uri = oauth2_provider.get_redirect_url(
        callback_url=str(request.url) + "callback/"
    )

    return RedirectResponse(redirect_uri)


@router.get('/{provider}/callback/', response_model=schema.token.Token)
def oauth2_provider_callback(
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

    user = crud.user.login(
            db,
            email=email,
            sub=sub,
            provider=provider
    )

    return auth.get_access_token(user.id)
