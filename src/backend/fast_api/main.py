from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.state import state_controller
from src.city import city_controller

ALLOWED_HOSTS = ["*"]

app = FastAPI(title="Bahamian Islands API", docs_url=None)

app.add_middleware(SessionMiddleware, secret_key="secret-string")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(state_controller.router)
app.include_router(city_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
