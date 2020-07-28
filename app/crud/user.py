from typing import Union, Optional
from app import auth, model, schema, exception
from .mixin import CrudBase


class CrudUser(CrudBase[model.User, schema.user.CreateUser, schema.user.UpdateUser]):

    def get_by_email(self, db, *, email: str) -> Optional[model.User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def login(
            self, db, *,
            email: str, password: str = None,
            sub: str = None, provider: str = None
            ) -> model.User:

        user = self.get_by_email(db, email=email)

        if user is not None:
            if (
                password is not None and
                auth.verify_password(password, user.password_hash)
            ):
                return user
            elif sub is not None and sub == user.sub and provider == user.provider:
                return user

        raise exception.wrong_credential

    def register(
            self, db, *,
            data: Union[schema.user.RegisterLocal, schema.user.RegisterProvider]
            ) -> model.User:

        user = self.get_by_email(db, email=data.email)

        if user is not None:
            raise exception.email_exists

        if getattr(data, 'password', None) is not None:
            password_hash = auth.get_password_hash(data.password)
            data = self.create_schema(**data.dict(), password_hash=password_hash)
        return self.create(db, data=data)


user = CrudUser(model.User, schema.user.CreateUser, schema.user.UpdateUser)
