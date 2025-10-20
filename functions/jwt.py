from jwt import encode, decode, exceptions#para hacer un jwt hay que instalar: pip install pyjwt
from datetime import datetime, timedelta, timezone
from os import getenv #con esta funcion importamos variables de entorno
from fastapi.responses import JSONResponse
from fastapi import status

def expired_date(hours:int):
    date = datetime.now(timezone.utc)
    print(date)
    new_date = date + timedelta(hours=hours)
    print(new_date) 
    return new_date

def write_token(data:dict):
    token = encode(payload={**data,"exp":expired_date(1)},key=getenv("SECRETORPRIVATEKEY"),algorithm="HS256")
    return token

def validate_token(token,output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRETORPRIVATEKEY"),algorithms=["HS256"])
        decode(token, key=getenv("SECRETORPRIVATEKEY"),algorithms=["HS256"])  
        return True  
    except exceptions.DecodeError:
        return JSONResponse(content={"message":"Invalid token"},status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message":"Token expired"},status_code=401)


