from fastapi import APIRouter, HTTPException
from starlette import status

from models.products import Category
from schemas.categories import CreateCategory, UpdateCategory

category_router = APIRouter()


@category_router.get('/categories')
async def get_categories():
    categories = await Category.all()
    return categories


@category_router.post('/categories')
async def create_product(category: CreateCategory):
    return await Category.create(**category.model_dump())


@category_router.patch('/categories/{categories_id}')
async def update_product(category_id: int, category: UpdateCategory):
    current_category = await Category.get(Category.id == category_id)
    if current_category:
        await Category.update(category_id, **category.model_dump(exclude_unset=True))
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    return f'Category updated'


@category_router.delete('/categories/{categories_id}')
async def delete_product(category_id: int):
    current_category = await Category.get(Category.id == category_id)
    if current_category:
        await Category.delete(category_id)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    return f'Category deleted'
