import usuarios.DAL.adUsuario as adUsuario
import usuarios.MODELS.etlUsuarios as etlUsuario
import usuarios.MODELS.etlexceptions as etlException
import usuarios.MODELS.etlapiResponse as etlApiResponse
import usuarios.MODELS.etlsecurity as etlSecurity

def createUser(user: etlUsuario.UserCreateModel):
    # Validar si existe el usuario - validar solo con username
    # Validar si la edad es mayor que 18, si es menor tiro error
    existUser = adUsuario.existUser(user.username)

    if existUser:
        raise etlException.BusinessError(1001, "El username ya existe")  

    if user.active == True:
        raise etlException.BusinessError(1003,"Solo se puede ingresar false")

    hashedPassword = etlSecurity.hash_password(user.password)
    
    adUsuario.createUser(user,hashedPassword)

    return etlApiResponse.ApiResponse()

def getAllUsers(): 

    listUsers : list[etlUsuario.GetAllUsersModel] = adUsuario.getAllUsers()

    return etlApiResponse.ApiResponse(
        data = {
            "totalUsers": len(listUsers),
            "users": listUsers
        }

    ) 

def login(username:str, password: str):
    user: etlUsuario.UserAuthModel = adUsuario.getUserByUsername(username)
    
    if user is None:
        raise etlException.BusinessError(1004,"Usuario o contraseña incorrectos")

    if not etlSecurity.verify_password(password, user.password):
        raise etlException.BusinessError(1004,"Usuario oss contraseña incorrectos")

    if user.active == False:
        raise etlException.BusinessError(1005,"El usuario está inactivo")

    # Quiero crear el token
    accessToken = etlSecurity.create_access_token(data={"sub": user.username})
    refreshToken = etlSecurity.create_refresh_token(data={"sub": user.username})

    return etlApiResponse.ApiResponse(
        data = etlUsuario.TokenModel
        (
            access_token=accessToken,
            refresh_token= refreshToken
        )
    )

def sumTwoNumbers(num1: int, num2: int):
    return num1 + num2

def alterCreateUser(user: etlUsuario.UserCreateModel):
    return user