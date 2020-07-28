# Example of OAuth2 register/login with FastAPI

With this example, register and login are possible using Google and Facebook OAuth2 as well as local OAuth2 (as explain in https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

Tools used: SQLAlchemy, oauthlib

## How to use

 1. Get an App Id and App Secret from Google and Facebook and set corresponding environment variable (or indicate them in app/setting.py)
 2. Create a folder and clone this repository inside
 3. Create a Python Virtual Environment and activate it:
  * Linux
 ```
 python -m venv venv
 source venv/bin/activate
 ```
  * Windows
  ```
  python -m venv venv
  venv\Scripts\activate
  ``` 
 4. Install requirements:
 ```
 pip install -r requirements.txt
 ```
 5. Start uvicorn or use run scripts provided
 
 Running script in dev mode (run dev or ./run.sh dev) set OAUTHLIB_INSECURE_TRANSPORT variable to 1 so oauthlib will not raise error if your are not using HTTPS https://oauthlib.readthedocs.io/en/latest/oauth2/security.html


## Sources

Some ideas from: 
 * FastAPI tutorials : https://fastapi.tiangolo.com/
 * https://realpython.com/flask-google-login/
 * https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
