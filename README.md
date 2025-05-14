## 🧩 Challenge

### 🛠 Chatbot personalizado con acceso a datos (LLM + RAG)

Implementa un mini chatbot (puede ser CLI o notebook) que, dado un input de usuario como:

> “¿Qué talla debería elegir para este abrigo?”
> 

...sea capaz de:

1. **Acceder a un perfil de cliente** (que te proporcionamos en JSON).
2. **Consultar información de un producto** (te damos una ficha técnica simulada).
3. **Responder** de forma coherente, justificando la talla sugerida.

**Requisitos mínimos:**

- Utilizar un LLM (puede ser OpenAI, Hugging Face u open-source).
- Simular una arquitectura tipo RAG (con búsqueda de contexto en datos estructurados).
- Incluir lógica para adaptar la recomendación según perfil de cliente.

**Extra (opcional):**

- Añadir memoria de conversación (por turnos).
- Manejar múltiples productos o clientes.