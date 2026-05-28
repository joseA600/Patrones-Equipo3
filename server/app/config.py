from pydantic import BaseModel


class Settings(BaseModel):
    """Configuracion central de la API."""

    app_name: str = "Patrones Equipo 3 API"
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
