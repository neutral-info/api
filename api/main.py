from api import v1
from api.backend.application import FastAPI

app = FastAPI()
app.include_router(v1.api_router)
