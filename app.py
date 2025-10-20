from fastapi import FastAPI
from config.db import meta,engine
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user
from dotenv import load_dotenv #esto es para cargar las variables de entorno y se instala: pip install python-dotenv

meta.create_all(engine)
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#Permite todos los orígenes 
    allow_credentials=True,
    allow_methods=["*"],#Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],#Permite todos los headers
)
load_dotenv()
app.include_router(user, prefix="/api")


