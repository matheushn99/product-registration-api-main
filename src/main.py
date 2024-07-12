from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse

from src.config.log_config import log_config
from src.controller.auth_controller import auth_router
from src.controller.product_controller import product_router

app = FastAPI(
    title="Product Registration API",
    description="API para gerenciar produtos",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Matheus Henrique",
        "email": "matheus.neres@fatec.sp.gov.br",
        "url": "https://github.com/matheushn99"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://github.com/matheushn99",
            "description": "Production server"
        }
    ]
)

app.include_router(product_router)
app.include_router(auth_router)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Um erro inesperado ocorreu no servidor"}
    )


@app.exception_handler(HTTPException)
async def general_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.get('/', tags=['Redirect'], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url='/docs')


@app.get('/docs', tags=['Redirect'], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="OpenApi UI"
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000, log_config=log_config)
