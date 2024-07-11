from fastapi import APIRouter, Depends, Header

from src.config.dependencies import get_authenticated_user, get_product_service
from src.domain.dto.dtos import ProdutoCreateDTO, ProdutoDTO, ProdutoUpdateDTO
from src.service.product_service import ProductService

product_router = APIRouter(prefix='/products', tags=['Products'], dependencies=[Depends(get_authenticated_user)])

@product_router.post(path='/',
                     status_code=201,
                     description='Cria Produto',
                     response_model=ProdutoDTO)
async def create(request: ProdutoCreateDTO, 
                 service: ProductService = Depends(get_product_service)
                 ):
    return service.create(request)

@product_router.get(path='/{user_id}',
                    status_code=200,
                    description='Busca Produto por id',
                    response_model=ProdutoDTO)
async def find_by_id(user_id: int, 
                     service: ProductService = Depends(get_product_service)):
    return service.find_by_id(user_id=user_id)


@product_router.get(path='/',
                    status_code=200,
                    description='Buscar Tosdos os produtos',
                    response_model=list[ProdutoDTO])
async def find_all(service: ProductService = Depends(get_product_service)):
    return service.find_all()


@product_router.put(path='/{user_id}',
                    status_code=200,
                    description='Atualizar Produto',
                    response_model=ProdutoDTO)
async def update(user_id: int, 
                 user_data: ProdutoUpdateDTO, 
                 service: ProductService = Depends(get_product_service)):
    return service.update(user_id, user_data)


@product_router.delete(path='/{user_id}',
                       status_code=204,
                       description='Deletar Produto por id')
async def delete(user_id: int, 
                 service: ProductService = Depends(get_product_service)):
    service.delete(user_id=user_id)
