from fastapi import HTTPException, status

#
# Generic
#
bad_request = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)


not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND
)


#
# Authentication
#
deactivated_user = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Your accound is deactivated",
    headers={"WWW-Authenticate": "Bearer"},
)


jwt_validation_fail = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


wrong_credential = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


#
# Register
#
email_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already used. Please choose another one.",
)
