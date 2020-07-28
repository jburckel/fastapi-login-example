from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class AppModelBase:

    @declared_attr
    def __tablename__(cls) -> str:
        """Table name is class name in snake case
        """
        return ''.join(
            '_' + c.lower() if index > 0 and c.isupper() else c.lower()
            for index, c in enumerate(cls.__name__)
        )
