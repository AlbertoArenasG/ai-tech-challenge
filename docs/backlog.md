# Backlog operativo

## 1. Fundamentos de datos y financiamiento
- [x] Ajustar `Car` y modelos relacionados para reflejar el CSV real.
- [x] Implementar `CatalogService.load_catalog` cargando el CSV al arrancar.
- [x] Implementar `CatalogService.search_cars` con filtros básicos por preferencia.
- [x] Completar `calculate_financing` con amortización y validaciones de rangos.

## 2. Servicios conversacionales
- [x] Definir contrato Pydantic para `/chat` (entrada/salida).
- [x] Diseñar prompts y `CommercialAgentService.answer` con integración a OpenAI.
- [x] Interpretar lenguaje natural para extraer preferencias y financiamiento.
 - [x] Incluir manejo de contexto (historial corto) para reducir alucinaciones.
 - [x] Persistir contexto a corto plazo con Redis para recordar datos del cliente.
- [x] Integrar la propuesta de valor de Kavak en el contexto (prompt o store) para FAQs fiables.

## 3. Integración WhatsApp/Twilio
- [x] Completar `parse_twilio_payload` y crear endpoint `/webhook/whatsapp`.
- [x] Preparar script o instrucciones para configurar el sandbox.

## 4. Hardening y DX
- [ ] Incorporar logging estructurado/errores (documentado en README).
- [x] Documentación de arquitectura y prompts (ver README + docs).
- [x] Propuesta de roadmap a producción (docs/roadmap.md).

## 5. Demo y entrega
- [ ] Crear colección o script de pruebas (curl/Thunder Client/Postman).
- [ ] Grabar o documentar el flujo del sandbox de WhatsApp.
- [ ] Revisar reproducibilidad: docker-compose, seeds, datos de ejemplo.
