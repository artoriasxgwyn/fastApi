from fastapi import Depends, HTTPException, status#Importaciones de FastAPI para manejar dependencias y excepciones HTTP
from fastapi.security import HTTPBearer#HTTPBearer es un esquema de seguridad que extrae el token del header Authorization
from functions.jwt import validate_token#Importamos nuestra función personalizada para validar tokens JWT
from fastapi.responses import JSONResponse#JSONResponse para manejar respuestas HTTP en formato JSON

# Crear una instancia de HTTPBearer para extraer tokens de tipo Bearer
# Esto automáticamente busca el token en el header: Authorization: Bearer <token>
security = HTTPBearer()

# Función dependencia que FastAPI ejecutará automáticamente en rutas protegidas
# Se ejecuta cuando una ruta incluye: current_user: dict = Depends(get_current_user)
async def get_current_user(token: str = Depends(security)):
    """
    Dependencia que valida el token JWT y retorna el payload si es válido
    Si el token es inválido, lanza una excepción HTTP 401
    """
    # Validar el token usando nuestra función personalizada
    # token.credentials extrae la parte del token (lo que viene después de "Bearer ")
    # output=True indica que queremos recibir el payload decodificado del token
    result = validate_token(token.credentials, output=True)
    # Si validate_token retorna un JSONResponse, significa que hubo un error
    # (token inválido, expirado, etc.)
    if isinstance(result, JSONResponse):
        # Extraer el mensaje de error del cuerpo de la respuesta JSON
        error_message = result.body.decode() if hasattr(result.body, 'decode') else "Token inválido"
        
        # Lanzar una excepción HTTP 401 (No autorizado)
        # Esto detendrá la ejecución de la ruta y retornará el error al cliente
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Código 401
            detail=error_message  # Mensaje de error descriptivo
        )
    
    # Si llegamos aquí, el token es válido
    # Retornamos el payload del token (datos del usuario: id, nombre, email, etc.)
    # Este payload estará disponible en la ruta como el parámetro 'current_user'
    return result