@echo off
IF "%1" == "set" GOTO set
IF "%1" == "dev" GOTO dev

:prod
uvicorn app.main:app
GOTO :EOF

:dev
set OAUTHLIB_INSECURE_TRANSPORT=1
uvicorn app.main:app --reload
set OAUTHLIB_INSECURE_TRANSPORT=
GOTO :EOF
