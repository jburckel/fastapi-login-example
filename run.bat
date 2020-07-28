@echo off
IF "%1" == "set" GOTO set
IF "%1" == "dev" GOTO dev

:prod
uvicorn app.main:app
GOTO :EOF

:set-env
set GOOGLE_CLIENT_ID=
set GOOGLE_CLIENT_SECRET=
set FACEBOOK_CLIENT_ID=
set FACEBOOK_CLIENT_SECRET=
GOTO :EOF

:dev
set OAUTHLIB_INSECURE_TRANSPORT=1
uvicorn app.main:app --reload
GOTO :EOF
