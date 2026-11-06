# Verificación desde una copia limpia

Fecha: 6 de noviembre de 2026. Plataforma: Windows, Python 3.12.14.

Se clonó el repositorio local en otra carpeta, sin .env, base SQLite ni índice Chroma. Se ejecutaron las instrucciones de preparación desde esa copia:

1. `python -m scripts.generate_mock_data`: 40 incidentes y 15 solicitantes.
2. `python -m scripts.seed_data`: base nueva con cinco tablas.
3. `python -m scripts.index_politicas`: seis políticas y cuatro casos.
4. `python -m pytest tests -q`: 38 pruebas aprobadas en 3,32 segundos.

La copia utilizó el entorno de dependencias ya instalado y el caché del modelo de embeddings. No se reinstalaron todas las dependencias en un segundo entorno. La comprobación de dependencias indicó `No broken requirements found` y sus versiones están fijadas en requirements-lock.txt.

La interfaz se verificó en Edge sin ventana: cuatro escenarios y una consulta real a Gemini, sin errores del navegador. Los escenarios completos con RAG están guardados en demo_resultados.json. La prueba independiente del agente completó dos turnos con Gemini 3.5 Flash, tres herramientas en el primer turno y continuidad en el segundo.
