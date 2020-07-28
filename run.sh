#!/bin/sh

if [ "$1" = "dev" ] | [ "$1" = "DEV" ]; then
  export OAUTHLIB_INSECURE_TRANSPORT=1
  uvicorn mpapi.main:app --reload
  unset OAUTHLIB_INSECURE_TRANSPORT
else
  uvicorn mpapi.main:app
fi
