#!/bin/sh

if [ "$1" = "dev" ] | [ "$1" = "DEV" ]; then
  export OAUTHLIB_INSECURE_TRANSPORT=1
  uvicorn app.main:app --reload
  unset OAUTHLIB_INSECURE_TRANSPORT
else
  uvicorn app.main:app
fi
