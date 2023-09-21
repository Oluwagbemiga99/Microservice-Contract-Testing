from config import get_settings
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import api_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(api_router,prefix='/api/v1')

if __name__ == "__main__":
    settings = get_settings()
    server = settings.server
    uvicorn.run(
        app="main:app",
        host=server.host,
        port=server.port,
        log_level=server.log_level,
        reload=server.reload,
    )
