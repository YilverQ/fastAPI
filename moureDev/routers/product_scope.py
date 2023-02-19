from fastapi import APIRouter

product = APIRouter(prefix='/product',
                    tags=['Product'])

@product.get('/all')
async def read_all():
    products_list = ['Producto 1', 'Producto 2', 'Producto 3']
    return {'detail' : 'Products API',
            'Products list' : products_list}