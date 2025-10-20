from fastapi import APIRouter, Response, Header, Depends #esta la funcion enrutadora de fastapi
from config.db import conn# esta es la funciona para conectarse
from models.user import users #Es la tabla
from schemas.user import User, UserLogin
import bcrypt  # Cambio aquí - bcrypt en lugar de Fernet pip install bcrypt
from starlette.status import HTTP_204_NO_CONTENT
from functions.jwt import write_token
from functions.dependencies import get_current_user

#datazo cloud clever devuelve las cosultas en tipo objet row asi que toca serializarlo

user=APIRouter()

@user.get("/users")
def get_users(current_user: dict = Depends(get_current_user)):
    try:
        print(f"Usuario autenticado: {current_user}")  
        #conn.rollback()
        result = conn.execute(users.select()).fetchall()
        users_list = []
        for row in result:
            users_list.append({
                "id": row.id,
                "name": row.name,
                "email": row.email
            })
        
        return users_list
        
    except Exception as e:
        return {"error": str(e)}

@user.get("/user/{id}")
def get_user_by_id(id:int):
    try:
        result = conn.execute(users.select().where(users.c.id == id)).first()#frist() es solo para consultas
        #print(result.id)
        user = {
            'user':{
             'id':result.id,
             'name':result.name,
             'email':result.email
            }
        }
        return user
    except Exception as e:
        return e

@user.post("/login")
def login(user: UserLogin):
    try:
        # Buscar usuario por nombre
        user_db = conn.execute(users.select().where(users.c.name == user.name)).first()
        if not user_db:
            return {"error": "Usuario no encontrado"}
        # Verificar contraseña con bcrypt
        if bcrypt.checkpw(user.password.encode("utf-8"), user_db.password.encode("utf-8")):
            print(user_db.id)
            user = {
                'id':user_db.id,
                'name':user_db.name,
                'email':user_db.email
                }
            return {"message": "Login exitoso", "user_id": user_db.id, "token":write_token(user)}
        else:
            return {"error": "Contraseña incorrecta"}
    except Exception as e:
        return {"error": f"Error en login: {str(e)}"}
    
@user.post("/users")
def create_user(user: User):
    try:
        new_user = dict(user)
        # Cambio aquí - bcrypt en lugar de Fernet
        hashed_password = bcrypt.hashpw(new_user["password"].encode("utf-8"), bcrypt.gensalt())#aca lo pasa a bytes para encriptarlo
        new_user["password"] = hashed_password.decode("utf-8")#aca lo trae de bytes a string para guardarlo en la base de datos
        
        result = conn.execute(users.insert().values(new_user))
        user_created = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
        conn.commit()
        return {
            "message": "Usuario creado exitosamente",
            "user": {
                "id": user_created.id,
                "name": user_created.name,
                "email": user_created.email
            }
        }    
    except Exception as e:
        conn.rollback()
        return {"error": f"Error al crear usuario: {str(e)}"}
    
@user.put("/users/{id}")
def update_user(id:int,user:User):
    try:
        print(user.name, id)
        # Cambio aquí - bcrypt en lugar de Fernet
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        
        conn.execute(users.update().where(users.c.id == id).values(
            name=user.name, 
            email=user.email, 
            password=hashed_password.decode("utf-8")
        ))
        result = conn.execute(users.select().where(users.c.id==id)).first()
        user = {
            "user":{
                 "name":user.name,
                 "email":user.email,
                 "password":user.password
                 }
                 }
        conn.commit()
        return user
    except Exception as e:
        return e

@user.delete("/users/{id}")
def delete_user(id:int):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)