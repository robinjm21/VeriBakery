# Veribakery API

API REST con FastAPI y SQLite para gestionar clientes.

## Requisitos
- Python 3.13 (o compatible)
- Git

## Instalación
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
```bash
uvicorn app.main:app --reload
```
- Base de datos SQLite `veribakery.db` se crea/actualiza automáticamente al iniciar.
- Documentación interactiva: `http://127.0.0.1:8000/docs`.

## Endpoints principales
- `GET /customers` (paginación, filtros, ordenación, header `X-Total-Count`)
- `POST /customers`
- `GET /customers/{id}`
- `PUT /customers/{id}`
- `PATCH /customers/{id}`
- `DELETE /customers/{id}`

## Paginación, filtros y ordenación
- Parámetros: `limit`, `offset`, `search`, `email`, `district`, `sort_by`, `order`.
- Ordenación: `sort_by` admite `id`, `name`, `email`, `phone`, `address`, `district`; `order` admite `asc`/`desc`.
- `X-Total-Count`: total de registros que coinciden con los filtros (antes de paginar).

## Notas
- `.gitignore` excluye `.venv`, `__pycache__`, `.env` y `veribakery.db`.
- Ajusta `git config user.name` y `git config user.email` a tus datos.