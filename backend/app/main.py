from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.errors import AppError
from app.routes.auth import router as auth_router

app = FastAPI(title="Expense Tracker API")


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


app.include_router(auth_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}