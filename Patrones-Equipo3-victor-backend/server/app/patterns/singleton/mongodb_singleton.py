from typing import Optional

from pymongo import MongoClient

from app.config import settings


class MongoDBSingleton:
    """Mantiene una sola instancia de MongoClient para toda la aplicacion."""

    _client: Optional[MongoClient] = None

    @classmethod
    def get_client(cls) -> MongoClient:
        """Crea el cliente una vez y reutiliza la misma conexion despues."""

        if cls._client is None:
            cls._client = MongoClient(
                settings.mongodb_uri,
                serverSelectionTimeoutMS=3000,
            )

        return cls._client
