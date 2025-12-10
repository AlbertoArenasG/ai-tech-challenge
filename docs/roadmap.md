# Roadmap hacia producción

## 1. Endurecer la API
- Firmar las peticiones de Twilio con el `X-Twilio-Signature` y rechazar peticiones no firmadas.
- Añadir logging estructurado (JSON) para `chat.request`/`chat.response` con IDs de conversación y métricas (latencia, tokens, costo).
- Trazas/alertas básicas (Prometheus u OpenTelemetry) para saber si el agente falla o excede tiempos.

## 2. Evaluación continua del agente
- Preparar un conjunto de conversaciones de referencia (scripts YAML) con expectativas sobre tono, factualidad y cobertura.
- Ejecutar estos scripts en CI usando `curl`/pytest + mocks de OpenAI para detectar regresiones.
- Medir satisfacción en producción con etiquetas manuales (thumbs-up/down) o keywords; almacenar en Redis o base ligera.

## 3. Despliegue y escalamiento
- Empaquetar en imagen oficial y desplegar en ECS con autoscaling (basado en CPU/latencia).
- Mover Redis a un servicio administrado (Elasticache) para alta disponibilidad.
- Usar Secrets Manager/Parameter Store para credenciales.

## 4. Procesos de QA antes de releases
- Pipeline CI: lint + pytest + pruebas de integración contra endpoints locales.
- Pipeline CD: despliegue en staging + smoke tests (colección HTTP) + verificación manual del sandbox de Twilio.
- Gate de aprobación: si algún escenario crítico falla o la evaluación automática detecta alucinaciones, bloquear release.

## 5. Experiencia de usuario y mejoras futuras
- Añadir un pequeño front (Web/Widget) para la demo, reutilizando `/chat`.
- Integrar embeddings + vector store opcional para enriquecer respuestas (FAQ extendidas) manteniendo el control del contexto.
- Cache de respuestas/prompt templates para reducir latencia/costo.
- Monitoreo de KPIs: tasa de conversión (solicitudes completadas), tasa de follow-up del agente, tiempos de respuesta.
