from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.infrastructure.api.routers.users import router as users_router

app = FastAPI(
    title="Hexagonal FastAPI",
    version="0.1.0",
    description="Clean Architecture Implementation",
)

app.include_router(users_router)

templates = Jinja2Templates(directory="src/infrastructure/api/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    health_status = "healthy" 

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "API Home",
            "health_status": health_status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
