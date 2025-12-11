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

Redis se levanta junto al bot (puedes inspeccionarlo en `localhost:6379` si necesitas revisar el estado de las conversaciones).  

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

El parser interno extrae marca, modelo, alias comunes (ej. “VW”), años y montos desde lenguaje natural, por lo que no es necesario enviar JSON estructurado cuando el mensaje llega desde WhatsApp.

Revisa `docs/manual_tests.md`
El detalle de componentes y roadmap está en `docs/architecture.md`, `docs/prompt_strategy.md` y `docs/roadmap.md`. para escenarios manuales que cubren `/chat` y el flujo de WhatsApp/Twilio.
El detalle de componentes y roadmap está en `docs/architecture.md`, `docs/prompt_strategy.md` y `docs/roadmap.md`.

### Webhook de WhatsApp
Configura el sandbox de Twilio para enviar mensajes HTTP POST a `http://<tu-host>/webhook/whatsapp` (usa `ngrok` si trabajas en local). El adaptador convertirá los campos `WaId`, `From` y `Body` en un `ChatRequest` y devolverá la respuesta del agente en texto plano para que Twilio la entregue al usuario.

## Notas adicionales
- El punto de entrada es `app/main.py`, el cual expone FastAPI con los endpoints `/health` y `/chat`.
- Si prefieres ejecutar sin Docker, instala las dependencias con `pip install -r requirements.txt` y corre `uvicorn app.main:app --reload`.

## Logging, Pruebas y Sandbox
- Las respuestas del agente se formatean en texto plano y se pueden inspeccionar usando `docker logs -f kavak-bot` (ver eventos `chat.request`/`chat.response`).
- También puedes llamar a `/chat` directamente con `curl` para ver el flujo en consola:
  ```bash
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"user_id": "demo", "message": "Busco un Vento 2019"}'
  ```
  A continuación ejecuta `docker logs -f kavak-bot` y verás entradas
  similares a:
  ```text
  INFO: {"event": "chat.request", "user": "demo", "channel": "direct", ...}
  INFO: {"event": "chat.response", "user": "demo", "channel": "direct", ...}
  ```
- Importa `docs/tests/postman_collection.json` en Postman/ThunderClient para ejecutar smoke tests (`/health`, `/chat` con catálogo y caso inválido).

### Sandbox Reproducible
1. Crea una cuenta de Twilio y activa el sandbox de WhatsApp.
2. Ejecuta `ngrok http 8000` y pega la URL HTTPS en el webhook (`/webhook/whatsapp`).
3. Desde tu teléfono envía `join <codigo>` al número de Twilio para vincularlo.
4. Usa los mensajes sugeridos de `docs/manual_tests.md` para validar el bot y observa los logs con `docker logs -f kavak-bot`.

## Arquitectura y Prompts
- Diagrama general: `docs/architecture_mermaid.md`.
- Flujo de prompts: `docs/prompt_flow_mermaid.md`.
- Detalles de componentes y estrategia en `docs/architecture.md` y `docs/prompt_strategy.md`.
- Roadmap y mejoras: `docs/roadmap.md`.
