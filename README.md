# AI Commercial Agent - Kavak Technical Assessment

## Puesta en marcha rápida
1. Copia tu archivo `.env` a partir de `.env.example` y completa las variables necesarias (`OPENAI_API_KEY`, rutas para el CSV y `VALUE_PROPOSITION_PATH`).
2. El catálogo de ejemplo ya vive en `app/data/catalog.csv`; ajusta las rutas del `.env` solo si deseas reemplazarlo con otro archivo.
3. Levanta el servicio con Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
4. Comprueba que el servidor esté operativo llamando al endpoint de salud:
   ```bash
   curl http://localhost:8000/health
   ```
   La respuesta esperada es `{"status":"ok"}`.

## Pruebas dentro del contenedor
Ejecuta la suite de pruebas directamente desde tu host (sin instalar Python) con:
```bash
docker exec -it kavak-bot pytest
```
Los tests viven bajo `tests/` y se copian dentro de la imagen, así que no necesitas preparar entornos locales.

## Conversar con el bot
Envía mensajes al endpoint principal:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "demo-user",
        "message": "Busco un SUV Toyota 2019 con menos de 80k km",
        "preferences": {"make": "Toyota", "max_km": 80000, "min_year": 2019},
        "financing": {"car_price": 350000, "down_payment": 70000, "years": 4}
      }'
```
La respuesta incluirá el texto generado por el agente y, si aplica, recomendaciones del catálogo y un plan de financiamiento.

## Notas adicionales
- El punto de entrada es `app/main.py`, el cual expone FastAPI con los endpoints `/health` y `/chat`.
- Si prefieres ejecutar sin Docker, instala las dependencias con `pip install -r requirements.txt` y corre `uvicorn app.main:app --reload`.
