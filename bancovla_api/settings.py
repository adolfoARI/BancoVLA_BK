import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT.lower() == "production"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-inseguro-solo-para-desarrollo")
DEBUG = not IS_PRODUCTION
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "*").split(",") if h.strip()]

INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "usuarios",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "bancovla_api.urls"
WSGI_APPLICATION = "bancovla_api.wsgi.application"

CORS_ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
    "EXCEPTION_HANDLER": "bancovla_api.exception_handler.business_error_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS" : [], 
        "APP_DIRS" : True, 
        "OPTIONS": {"context_processors": []},
    },
]

STATIC_URL = "static/"

SPECTACULAR_SETTINGS = {
    "TITLE": "BancoVLA API V1 Johel",
    "DESCRIPTION": "API de usuarios y autenticación del Banco VLA - Despliegue Automatico de Adolfo",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,   
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}

LANGUAGE_CODE = "es"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
