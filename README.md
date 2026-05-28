# Patrones Equipo 3

Proyecto base con frontend en React + Vite y backend en FastAPI.

## Estructura principal

```text
client/
  src/
    components/
    pages/
    routes/
    services/

server/
  app/
    models/
    patterns/
    routes/
    services/
  main.py
  requirements.txt
```

## Backend

```bash
cd server
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`.

## Frontend

```bash
cd client
npm install
npm run dev
```

El cliente queda disponible en `http://localhost:5173`.

## Notas

- CORS esta configurado para el cliente local de Vite.
- No se implementa MongoDB todavia.
- La estructura queda preparada para agregar modelos, rutas, servicios y patrones de diseno de forma ordenada.
