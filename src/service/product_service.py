import logging

from fastapi import HTTPException
from psycopg2 import IntegrityError
from pydantic import TypeAdapter

from src.domain.dto.dtos import ProdutoCreateDTO, ProdutoDTO, ProdutoUpdateDTO
from src.domain.model.models import Product
from src.repository.usuario_repository import ProductRepository


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create(self, data: ProdutoCreateDTO) -> ProdutoDTO:
        logging.info('Criando produto')
        product = Product(**data.model_dump())
        try:
            created = self.repository.save(product)
            return TypeAdapter(ProdutoDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar produto: {data.model_dump()}')
            raise HTTPException(status_code=409, 
                                detail=f'Produto já existe na base: {e.args[0]}')
        
    def read(self, user_id: int) -> ProdutoDTO:
        logging.info('Buscando um Produto.')
        return TypeAdapter(ProdutoDTO).validate_python(self._read(user_id))
        
    def _read(self, user_id: int) -> Product:
        product = self.repository.read(user_id)
        if product is None:
            logging.error(f'Usuário {user_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Produto {user_id} não encontrado.')
        return product

    def find_by_id(self, user_id: int) -> ProdutoDTO:
        logging.info(f'Buscando produto com ID {user_id}')
        return TypeAdapter(ProdutoDTO).validate_python(self._read(user_id))

    def find_all(self) -> list[ProdutoDTO]:
        logging.info('Buscando todos os produtos')
        products = self.repository.find_all()
        return [TypeAdapter(ProdutoDTO).validate_python(product) for product in products]

    def update(self, user_id: int, user_data: ProdutoUpdateDTO) -> ProdutoDTO:
        logging.info(f'Atualizando produto com ID {user_id}')
        product = self._read(user_id)
        data = user_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(product,key,value)
        product_updated = self.repository.save(product)
        logging.info(f'Produto {user_id} atualizado: {product_updated}')
        return TypeAdapter(ProdutoDTO).validate_python(product_updated)

    def delete(self, user_id: int) -> int:
        logging.info(f'Deletando produto com ID {user_id}')
        product = self._read(user_id)
        self.repository.delete(product)
        logging.info(f'Produto {user_id} deletado')
        return user_id
