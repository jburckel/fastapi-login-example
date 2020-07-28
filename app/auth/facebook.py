from app.setting import settings
from .provider_generic import OAuth2

oauth2 = OAuth2(
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    authorization_url="https://www.facebook.com/dialog/oauth",
    token_url="https://graph.facebook.com/oauth/access_token",
    userinfo_url="https://graph.facebook.com/me?fields=email",
    scope=["email", "public_profile"]
)
