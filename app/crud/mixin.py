from typing import Generic, TypeVar

from app import exception
from app.model import AppModelBase
from app.schema import AppSchemaBase

ModelType = TypeVar("ModelType", bound=AppModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=AppSchemaBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=AppSchemaBase)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
            self, model: ModelType,
            create_schema: CreateSchemaType, update_schema: UpdateSchemaType
            ):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema

    def get(self, db, *, id=id) -> ModelType:
        record = db.query(self.model).get(id)
        if record is None:
            raise exception.not_found
        return record

    def create(self, db, *, data: CreateSchemaType) -> ModelType:
        print(type(data), type(self.create_schema))
        if not isinstance(data, self.create_schema):
            data = self.create_schema(**data.dict())
        record = self.model(**data.dict())
        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    def update(self, db, *, id: int, data: UpdateSchemaType) -> ModelType:
        record = self.get(db, id=id)
        if not isinstance(data, self.create_schema):
            data = self.update_schema(**data.dict())
        data_dict = data.dict(exclude_unset=True)
        for key in data_dict.keys():
            setattr(record, key, data_dict[key])
        db.commit()
        db.refresh(record)
        return record

    def delete(self, db, *, id: int) -> ModelType:
        record = self.get(id)
        db.delete(record)
        db.commit()
        return record
