"""
Application entrypoint.

Run with:
    uvicorn app.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown hooks."""
    settings = get_settings()
    logger.info("Starting %s", settings.app_name)
    logger.info("Upload dir: %s", settings.upload_dir)
    logger.info("Generated dir: %s", settings.generated_dir)
    logger.info("Metadata dir: %s", settings.metadata_dir)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="AI-powered backend that generates photorealistic product scene images.",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.112.13.91:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    # Consistent JSON error envelope for all HTTPExceptions.
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.error("HTTPException | path=%s | status=%s | detail=%s", request.url.path, exc.status_code, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "detail": None},
        )

    # Catch-all safety net so raw exceptions are never leaked to clients.
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception | path=%s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error.", "detail": None},
        )

    app.include_router(api_router)

    # Serve generated images as static files, e.g. GET /generated/<uuid>.png
    app.mount(
        "/generated",
        StaticFiles(directory=str(settings.generated_dir)),
        name="generated",
    )

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """Simple liveness endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
