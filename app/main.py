from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import expenses, users, currency
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(currency.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Expense Tracker API",
        version="1.0.0",
        description="This is a simple API to track expenses with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]  
    field = ".".join(str(loc) for loc in first_error["loc"][1:])  
    error_message = first_error["msg"]  

    return JSONResponse(
        status_code=400,
        content={
            "error": field,
            "success": False,
            "statuscode": 400,
            "message": error_message
        }
    )