# Patrones Equipo 3

Sistema academico para administrar materiales, prestamos, devoluciones,
mantenimiento y bitacora. El proyecto usa React + Vite en el frontend,
FastAPI en el backend y MongoDB como base de datos.

integrantes de el equipo:
-Acevedo Garcia Jose Antonio 
-osorio hernandez brian lisandro
-victor manuel 
-velazco martinez candy heidy

## Tecnologias

- React con Vite
- React Router
- Axios
- FastAPI
- PyMongo
- MongoDB

## Patrones Implementados

- Singleton: reutiliza una unica conexion de MongoDB.
- Factory Method: crea materiales por tipo (`Laptop`, `Router`, `Proyector`, `Adaptador`, `Cable`).
- State: valida cambios entre `Disponible`, `Prestado`, `EnMantenimiento` y `DadoDeBaja`.
- Observer: registra eventos automaticos en la bitacora.
- Command: encapsula prestar, devolver y enviar a mantenimiento.

## Estructura Principal

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
    routes/
    services/
  patterns/
    command/
    observer/
    state/
  main.py
  requirements.txt
  .env.example
```

## Instalacion Backend

```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Variables principales:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=patrones_equipo3
```

La API queda disponible en `http://localhost:8000`.

## Instalacion Frontend

```bash
cd client
npm install
npm run dev
```

El cliente queda disponible en `http://localhost:5173`.

## Endpoints Principales

- `GET /health`
- `GET /db-status`
- `GET /materiales`
- `POST /materiales`
- `GET /materiales/disponibles`
- `PUT /materiales/{id}/mantenimiento`
- `POST /prestamos`
- `GET /prestamos`
- `PUT /prestamos/{id}/devolver`
- `GET /bitacora`

## Flujo General

1. Registrar materiales desde la pagina Materiales.
2. Prestar materiales disponibles desde Prestamos.
3. Registrar devoluciones desde Prestamos.
4. Enviar materiales a mantenimiento.
5. Consultar reportes y bitacora.

## Notas de Entrega

- El frontend consume el backend con Axios desde `client/src/services`.
- La bitacora se genera automaticamente mediante Observer.
- Las transiciones invalidas se bloquean en backend mediante State.
- Las acciones principales se encapsulan con Command.
