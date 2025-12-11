# Escenarios de prueba manual

## 1. Endpoint `/chat`
1. **Consulta de catálogo**
   - Enviar el `curl` del README (SUV Toyota).
   - Verificar que el campo `recommendations` traiga vehículos y que el mensaje cite la propuesta de valor solo cuando corresponda.
2. **Pregunta sobre propuesta de valor**
   - Payload mínimo: `{ "user_id": "qa", "message": "¿Cuál es la propuesta de valor de Kavak?" }`.
   - Esperado: respuesta basada únicamente en `app/data/value_proposition.md`.
3. **Validación de financiamiento**
   - Enviar `years` fuera del rango. Esperar `400 Bad Request`.
4. **Colección automática (Postman/ThunderClient)**
   - Importar `/docs/tests/postman_collection.json` y ejecutar las peticiones `chat_health`, `chat_catalog`, `chat_finance_invalid`.

## 2. WhatsApp/Twilio
1. Configurar el sandbox de Twilio y apuntar el webhook a `https://<tu-ngrok>/webhook/whatsapp`.
2. Crear una cuenta de Twilio, activar el sandbox de WhatsApp y conectar el número de prueba.
3. Ejecutar `ngrok http 8000` y copiar la URL HTTPS en el webhook.
4. Enviar `join <codigo>` al número de Twilio y usa los mensajes sugeridos para validar el bot en tiempo real.
5. Revisar logs en `docker logs -f kavak-bot` para observar `chat.request`/`chat.response`.

   - Crear una cuenta en Twilio, activar el sandbox de WhatsApp y conectar el número de prueba.
   - Ejecutar `ngrok http 8000` y copiar la URL HTTPS en el webhook del sandbox.
   - Enviar `join <codigo>` al número de Twilio desde tu teléfono.
   - Vale reproducir los mensajes anteriores y revisar el bot en tiempo real.
