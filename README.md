# Example of OAuth2 register/login with FastAPI

With this example, register and login are possible using Google and Facebook OAuth2 as well as local OAuth2 (as explain in https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

Tools and libraries used: SQLAlchemy, oauthlib

## How to use

 1. Get an App Id and App Secret from Google and Facebook and set corresponding environment variable (or indicate them in app/setting.py) 
 2. Install requirements:
 ```
 pip install -r requirements.txt
 ```


## Sources

Some ideas from: 
 * https://realpython.com/flask-google-login/
 * https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
