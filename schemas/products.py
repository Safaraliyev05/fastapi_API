from pydantic import BaseModel


class BaseProduct(BaseModel):
    id: int


class CreateProduct(BaseModel):
    name: str
    description: str | None = None
    price: int
    quantity: int
    category_id: int

    class Config:
        from_attributes = True


class ResponseProduct(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True


class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

    class Config:
        from_attributes = True



