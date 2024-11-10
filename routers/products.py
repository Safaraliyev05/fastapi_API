import time

from fastapi import APIRouter, Query, HTTPException, status
from sqlalchemy import func
from sqlalchemy.future import select
from starlette.requests import Request

from models import Product
from models.products import Category
from schemas import CreateProduct, ResponseProduct, UpdateProduct

shop_router = APIRouter()


@shop_router.post('/products')
async def create_product(product: CreateProduct) -> ResponseProduct:
    return await Product.create(**product.model_dump())


@shop_router.patch('/products/{product_id}')
async def update_product(product_id: int, product: UpdateProduct):
    current_product = await Product.get(Product.id == product_id)
    if current_product:
        await Product.update(product_id, **product.model_dump(exclude_unset=True))
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return f'Product updated'


@shop_router.delete('/products/{product_id}')
async def delete_product(product_id: int):
    current_product = await Product.get(Product.id == product_id)
    if current_product:
        await Product.delete(product_id)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return "Product deleted"


@shop_router.get('/products')
async def get_products(
        name: str = Query(None, description="Name of the product to search for"),
        min_price: int = Query(None, description="Minimum price filter"),
        max_price: int = Query(None, description="Maximum price filter"),
        category: str = Query(None, description='Category name'),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Number of products per page"),
):
    query = select(Product)

    if name:
        query = query.where(Product.name.ilike(f'%{name}%'))
    if min_price:
        query = query.where(Product.price >= min_price)
    if max_price:
        query = query.where(Product.price <= max_price)
    if category:
        query = query.join(Category).where(Category.name.ilike(f'%{category}%'))

    offset = (page - 1) * page_size

    query = query.offset(offset).limit(page_size)
    products = await Product.run_query(query)

    total_query = select(func.count()).select_from(Product)
    if name:
        total_query = total_query.where(Product.name.ilike(f'%{name}%'))
    if min_price:
        total_query = total_query.where(Product.price >= min_price)
    if max_price:
        total_query = total_query.where(Product.price <= max_price)

    total_count = await Product.query_count(total_query)

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "products": products
    }


@shop_router.get("/generate", name='generate_products')
async def generate_products(request: Request):
    data = {
        'product': Product
    }

    start = time.time()

    for k, count in dict(request.query_params).items():
        if k in data:
            await data[k].generate(int(count))

    end = time.time()
    return {"message": "OK", "spend_time": int(end - start)}
