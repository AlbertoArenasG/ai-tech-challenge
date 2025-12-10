# Backlog operativo

## 1. Fundamentos de datos y financiamiento
- [x] Ajustar `Car` y modelos relacionados para reflejar el CSV real.
- [x] Implementar `CatalogService.load_catalog` cargando el CSV al arrancar.
- [x] Implementar `CatalogService.search_cars` con filtros básicos por preferencia.
- [ ] Completar `calculate_financing` con amortización y validaciones de rangos.

## 2. Servicios conversacionales
- [ ] Definir contrato Pydantic para `/chat` (entrada/salida).
- [ ] Diseñar prompts y `CommercialAgentService.answer` con integración a OpenAI.
- [ ] Incluir manejo de contexto (historial corto) para reducir alucinaciones.
- [ ] Integrar la propuesta de valor de Kavak en el contexto (prompt o store) para FAQs fiables.

## 3. Integración WhatsApp/Twilio
- [ ] Completar `parse_twilio_payload` y crear endpoint `/webhook/whatsapp`.
- [ ] Firmar/validar las peticiones de Twilio (token, firmas).
- [ ] Preparar script o instrucciones para configurar el sandbox.

## 4. Hardening y DX
- [ ] Añadir pruebas unitarias para catálogo y financiamiento.
- [x] Cobertura inicial de catálogo.
- [ ] Cobertura de financiamiento.
- [ ] Incorporar logging estructurado y manejo de errores consistente.
- [ ] Documentar arquitectura y prompts (diagramas + README extendido).
- [ ] Proponer roadmap a producción (deploy, evaluación continua, regresiones).

## 5. Demo y entrega
- [ ] Crear colección o script de pruebas (curl/Thunder Client/Postman).
- [ ] Grabar o documentar el flujo del sandbox de WhatsApp.
- [ ] Revisar reproducibilidad: docker-compose, seeds, datos de ejemplo.
