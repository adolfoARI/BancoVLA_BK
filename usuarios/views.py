from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

import usuarios.MODELS.etlUsuarios as etlUsuario
import usuarios.MODELS.etlsecurity as etlSecurity
import usuarios.MODELS.etlapiResponse as etlApiResponse
import usuarios.BLL.lnUsuarios as lnUsuario
import usuarios.MODELS.etlDocs as etlDocs

#Requisito de seguridad que referencia el esquema
BEARER = [{"BearerAuth": []}]


@extend_schema(
    tags=["Autenticación"],
    summary="Iniciar sesión",
    description="Valida credenciales y devuelve un access token y un refresh token.",
    request=etlUsuario.LoginModel.drf_serializer,
    responses={
        200: etlDocs.TokenResponse.drf_serializer,
        400: etlDocs.MessageResponse.drf_serializer,
    },
    auth=[],
)
@api_view(["POST"])
def login(request):
    user = etlUsuario.LoginModel.model_validate(request.data)
    response = lnUsuario.login(user.username, user.password)
    return Response(response.model_dump(mode="json"))

@extend_schema(
    tags=["Usuarios"],
    summary="Crear un usuario",
    description="Registra un usuario nuevo. La contraseña se guarda hasheada con bcrypt.",
    request=etlUsuario.UserCreateModel.drf_serializer,
    responses={
        200: etlDocs.MessageResponse.drf_serializer,
        400: etlDocs.MessageResponse.drf_serializer,
    },
    auth=[],
)
@api_view(["POST"])
def createNewUser(request):
    user = etlUsuario.UserCreateModel.model_validate(request.data)
    response = lnUsuario.createUser(user)
    return Response(response.model_dump(mode="json"))


@extend_schema(
    tags=["Usuarios"],
    summary="Listar todos los usuarios",
    description="Requiere un access token válido en el header Authorization.",
    request=None,
    responses={
        200: etlDocs.UserResponse.drf_serializer,
        401: etlDocs.MessageResponse.drf_serializer,
    },
    auth=BEARER,
)
@api_view(["POST"])
def getAllUsers(request):
    currentUser = etlSecurity.get_current_user(request)    
    response = lnUsuario.getAllUsers()
    return Response(response.model_dump(mode="json"))


@extend_schema(
    tags=["Autenticación"],
    summary="Renovar el access token",
    description="Recibe el refresh token en el header Authorization y emite un access token nuevo.",
    request=None,
    responses={
        200: etlDocs.TokenResponse.drf_serializer,
        401: etlDocs.MessageResponse.drf_serializer,
    },
    auth=BEARER,
)
@api_view(["POST"])
def refresh_token(request):
    currentUser = etlSecurity.get_current_user(request)   
    newAccessToken = etlSecurity.create_access_token(data = {"sub": currentUser})

    response = etlApiResponse.ApiResponse(
        data = etlUsuario.TokenModel(
            access_token=newAccessToken, 
            refresh_token="", 
            token_type="bearer"
        )
    )
     
    return Response(response.model_dump(mode="json"))

