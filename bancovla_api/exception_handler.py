from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

import usuarios.MODELS.etlexceptions as etlException

def business_error_handler(exc, context):
    """
        Equivalente @app.exception_handler de FastAPI

        {"codigo":..., "mensaje":...} con su status_code
    """

    if isinstance(exc, etlException.BusinessError):
        return Response(
            {
                "codigo": exc.codigo,
                "mensaje" :exc.mensaje
            },
            status=exc.status_code
        )

    #Se cayó la base de datos
    if isinstance(exc, ValidationError):
         return Response(
                    {
                        "codigo": 1000,
                        "mensaje" :exc.mensaje
                    },
                    status=exc.status_code
                )

    return drf_exception_handler(exc, context)