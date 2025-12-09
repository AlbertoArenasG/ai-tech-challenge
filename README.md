# AI Commercial Agent - Kavak Technical Assessment

## Puesta en marcha rápida
1. Copia tu archivo `.env` a partir de `.env.example` y completa las variables necesarias (`OPENAI_API_KEY`, rutas para el CSV).
2. El catálogo de ejemplo ya vive en `app/data/catalog.csv`; ajusta las rutas del `.env` solo si deseas reemplazarlo con otro archivo.
3. Levanta el servicio con Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Comprueba que el servidor esté operativo llamando al endpoint de salud:
   ```bash
   curl http://localhost:8000/health
   ```
   La respuesta esperada es `{"status":"ok"}`.

## Notas adicionales
- El punto de entrada es `app/main.py`, el cual expone FastAPI con los endpoints `/health` y `/chat`.
- Si prefieres ejecutar sin Docker, instala las dependencias con `pip install -r requirements.txt` y corre `uvicorn app.main:app --reload`.
