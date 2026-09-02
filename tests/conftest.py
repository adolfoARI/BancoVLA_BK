"""
Configuracion compartida por todas las pruebas
El DAL se mockea siempre: ninguna prueba toca la base de datos real
"""

import pytest
from rest_framework.test import APIClient
import usuarios.DAL.adUsuario as adUsuario

@pytest.fixture
def client():
    """Cliente http para probar los endpoints sin levantar el servidor"""
    return APIClient()

@pytest.fixture
def bloquear_base_real(monkeypatch):

    def _prohibido(*args, **kwargs):
        raise AssertionError(
            "Una prueba intento abrir una conexion real a la base de datos"
        )

    monkeypatch.setattr(adUsuario, "getConnection", _prohibido)