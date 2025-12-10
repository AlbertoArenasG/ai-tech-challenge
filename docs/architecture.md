# Arquitectura de Alto Nivel

```
┌────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ WhatsApp + │     │ FastAPI Bot  │     │ OpenAI / Redis /    │
│ Twilio     │────▶│ (app/main.py)│────▶│ Servicios internos  │
└────────────┘     └──────────────┘     └─────────────────────┘
       │                  │                             │
       │                  │                             ├─ CatalogService (CSV en memoria)
       │                  │                             ├─ CommercialAgentService (prompts)
       │                  │                             ├─ ConversationStore (Redis)
       │                  │                             └─ IntentClassifier (OpenAI)
       │                  │
       └──── respuestas ◀─┴─────────────────────────────┘
```

## Componentes
- **Adapters** (`app/adapters/whatsapp_adapter.py`): normalizan las peticiones y formatean respuestas planas compatibles con Twilio.
- **API** (`app/main.py`): valida payloads (`ChatRequest`), aplica el parser de lenguaje natural y coordina llamadas al `CommercialAgentService`.
- **Servicios**:
  - `MessageParser`: infiere marca/modelo, detecta campos faltantes.
  - `CatalogService`: carga el CSV al arrancar, provee búsquedas y alternativas.
  - `CommercialAgentService`: construye prompts, genera recomendaciones y planes.
  - `ConversationStore`: persiste preferencias/historial en Redis.
  - `IntentClassifier`: primer guardia para saber si el mensaje es saludo, financiamiento, etc.
- **Datos**: `app/data/catalog.csv` + `app/data/value_proposition.md`.

## Flujo resumido
1. Twilio envía `WaId`, `From`, `Body` → `/webhook/whatsapp`.
2. El adaptador genera un `ChatRequest` y la API aplica `MessageParser` + `ConversationStore`.
3. `IntentClassifier` categoriza; según el resultado, se envía al `CommercialAgentService` con las opciones/perfiles correctos.
4. El agente consulta Catalog/Finance, arma el prompt y responde.
5. El adaptador devuelve texto plano a Twilio, que responde al usuario.
