# Estrategia de Prompts y Control de Alucinaciones

1. **Clasificación**: el primer mensaje se clasifica con un LLM ligero (`IntentClassifier`) para saber si es saludo, small talk, recomendación, financiamiento, FAQ u off-topic. Esto permite mantener un tono adecuado y no responder fuera de contexto.
2. **Contexto autorizado**: el `CommercialAgentService` concatena únicamente:
   - Propuesta de valor (`value_proposition.md`).
   - Resumen de recomendaciones del catálogo o alternativas cercanas.
   - Plan de financiamiento calculado.
   - Datos faltantes y opciones válidas (listas cerradas).
3. **Instrucciones del sistema**: prohibimos inventar datos (“Solo puedes responder con el contexto autorizado… si falta información, dilo y pregunta”). Además se exige ofrecer alternativas cuando no hay coincidencias.
4. **Post-procesamiento**: el adaptador recorta la respuesta a 1,500 caracteres y evita duplicar bullets; si falta información (marca/modelo), la API pregunta con listas del catálogo.
5. **Roadmap**: en producción, los prompts se versionan en Git y se evalúan automáticamente con scripts, de modo que cualquier ajuste pase por QA antes de llegar a Twilio.
