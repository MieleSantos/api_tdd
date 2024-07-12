from fastapi import FastAPI

from store.routers import api_router

app = FastAPI()
# app = FastAPI(
#    version="0.0.1",
#    title=settings.PROJECT_NAME,
#    root_path=settings.ROOT_PATH,
# )
app.include_router(api_router)
