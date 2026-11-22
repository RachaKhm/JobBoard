"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
Second instance (another port):
      uvicorn app.main:app --port 8094
  or: $env:PORT=8094; python -m app.main
"""
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client

from app.routers import notification



def _resolve_port(default: int = 8084) -> int:
    """Port of this instance, also used for the Eureka registration.

    Priority: PORT environment variable > --port argument of uvicorn > 8084.
    This way the port announced to Eureka is always the port the service
    really listens on, whatever the launch command.
    """
    env_port = os.getenv("PORT")
    if env_port:
        return int(env_port)
    args = sys.argv
    for i, arg in enumerate(args):
        if arg == "--port" and i + 1 < len(args):
            return int(args[i + 1])
        if arg.startswith("--port="):
            return int(arg.split("=", 1)[1])
    return default


PORT = _resolve_port()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="NOTIFICATION",
        instance_host="localhost",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info",
        home_page_url=f"http://localhost:{PORT}/",
    )
    print(f"Service NOTIFICATION registered on port {PORT}")

    try:
        yield
    finally:
        await eureka_client.stop_async()
        print("Service NOTIFICATION deregistered from Eureka")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
    lifespan=lifespan,
)

app.include_router(notification.router)


# ---- Health & info (équivalent de /actuator/health et /actuator/info) ----
@app.get("/health", tags=["Monitoring"], summary="Etat de santé du service")
def health() -> dict:
    return {"status": "UP"}


@app.get("/info", tags=["Monitoring"], summary="Informations sur le service")
def info() -> dict:
    return {
        "app": {
            "name": "notification",
            "version": app.version,
            "description": "Microservice de gestion des notifications",
        }
    }

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
