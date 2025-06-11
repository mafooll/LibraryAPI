from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"
