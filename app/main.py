from fastapi import FastAPI
from app.routes import router
from app.auth import router as auth_router
from app.db import engine, Base
from app import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todofrontend-3foej5jzp-oladejifalade-7202s-projects.vercel.app",
        "https://todolist-psi-one-45.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is working"}


app.include_router(auth_router)
app.include_router(router)
