from pymongo.database import Database

from app.config import settings
from app.patterns.singleton import MongoDBSingleton


def get_database() -> Database:
    """Devuelve una instancia reutilizable de la base de datos configurada."""

    client = MongoDBSingleton.get_client()

    return client[settings.mongodb_database]


def check_database_connection() -> dict[str, str]:
    """Ejecuta un ping simple para validar conectividad con MongoDB."""

    try:
        MongoDBSingleton.get_client().admin.command("ping")
        return {
            "status": "ok",
            "message": "Conexion a MongoDB activa",
            "database": settings.mongodb_database,
        }
    except Exception as error:
        return {
            "status": "error",
            "message": f"No se pudo conectar a MongoDB: {error}",
            "database": settings.mongodb_database,
        }
