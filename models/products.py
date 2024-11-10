from faker import Faker
from sqlalchemy import String, VARCHAR, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.database import CreatedBaseModel

fake = Faker()


class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category', lazy='selectin')


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, server_default="0")

    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', lazy='selectin', back_populates='products')

    @classmethod
    async def generate(cls, count: int = 1):
        for _ in range(count):
            await cls.create(
                name=fake.company(),
                description=fake.sentence(),
                price=fake.random_int(min=1, max=100),
                quantity=fake.random_int(min=0, max=50)
            )
