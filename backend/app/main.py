from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.errors import AppError
from app.routes.auth import router as auth_router
from app.routes.expenses import router as expenses_router
from app.logging_config import setup_logging, logger
import time
import uuid

setup_logging()
app = FastAPI(title="Expense Tracker API")


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()
    logger.info("request_started", path=request.url.path, method=request.method, request_id=request_id)
    response = await call_next(request)
    latency_ms = round((time.time() - start) * 1000)
    logger.info("request_finished", status=response.status_code, latency_ms=latency_ms, request_id=request_id)
    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(auth_router)
app.include_router(expenses_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}