from fastapi import APIRouter

# Criar o roteador principal da API
api_router = APIRouter()

# Aqui serão incluídos os roteadores dos módulos
# Exemplo:
# api_router.include_router(
#     product.router, prefix="/products", tags=["products"]
# )
