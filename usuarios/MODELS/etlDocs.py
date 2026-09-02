"""
    Modelos usados unicamente para documentar la api en swagger. 
    No participan en la logica de negocio: describir la forma que ya tiene
    la respuesta que arma ApiResponse
"""

from typing import Optional, List
from drf_pydantic import BaseModel

from usuarios.MODELS.etlUsuarios import TokenModel, GetAllUsersModel

class MessageResponse(BaseModel):
    codigo:int =0
    mensaje: str = "Transaccion exitosa"

class TokenResponse(BaseModel):
    """ Respuesta /Login y /Refresh"""
    codigo :int= 0
    mensaje: str = "Transaccion exitosa"
    data: Optional[TokenModel] = None

class UsersPayLoad(BaseModel):
    totalUsers:int
    users: List[GetAllUsersModel]

class UserResponse(BaseModel):
    """Respuesta /GetAllUsers"""
    codigo :int = 0
    mensaje: str = "Transaccion exitosa"
    data : Optional[UsersPayLoad] = None