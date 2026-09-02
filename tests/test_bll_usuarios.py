import pytest
from datetime import date
from jose import jwt

import usuarios.BLL.lnUsuarios as lnUsuario
import usuarios.DAL.adUsuario as adUsuario
import usuarios.MODELS.etlUsuarios as etlUsuario
import usuarios.MODELS.etlsecurity as etlSecurity
import usuarios.MODELS.etlexceptions as etlException

@pytest.fixture
def usuarioNuevo():
    return etlUsuario.UserCreateModel(
        name="Adolfo",
        birthdate=date(1992,12,21),
        active=False, 
        username= "jvargas", 
        password="miClave123"
    )

#===================================
# createUser
#===================================

def test_createUser_guarda_devuelve_codigo_0(monkeypatch, usuarioNuevo):
    llamadas = []

    monkeypatch.setattr(adUsuario, "existUser", lambda username:False)
    monkeypatch.setattr(
        adUsuario, "createUser",
        lambda user, hashedPassword: llamadas.append((user, hashedPassword))
    )

    response = lnUsuario.createUser(usuarioNuevo)

    assert response.codigo == 0
    assert response.mensaje == "Transaccion exitosa"
    assert len(llamadas) == 1


#==================================
# getAllUsers
#==================================

def test_getAllUsers_flujo_correcto(monkeypatch):
    usuarios = [
        etlUsuario.GetAllUsersModel(idUser=1, username="jvargas", name="Adolfo", active=True),
        etlUsuario.GetAllUsersModel(idUser=2, username="sophia03", name="Sophia", active=False),
    ]

    monkeypatch.setattr(adUsuario, "getAllUsers", lambda: usuarios)

    response = lnUsuario.getAllUsers()

    assert response.codigo == 0
    assert response.data["totalUsers"] == 2
    assert response.data["users"][0].username == "jvargas"