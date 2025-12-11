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
2. Mensajes sugeridos:
   - "Hola, busco un sedán 2019 con menos de 60k km" → debería responder con recomendaciones.
   - "¿Qué beneficios ofrece Kavak?" → debe contestar solo con la propuesta de valor.
   - "Cotiza un financiamiento para 400k con 80k de enganche a 4 años" → revisar que llegue el plan.
3. Revisar logs en `docker logs -f kavak-bot` para observar `chat.request`/`chat.response` (cuando se agreguen) y las respuestas enviadas a Twilio.
