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

---

## 📝 Información General

**simpleshop-rag** es un chatbot basado en LLM (OpenAI) y arquitectura RAG, diseñado para recomendar productos de moda personalizados según el perfil del cliente y el catálogo de productos. Utiliza almacenamiento vectorial para búsquedas contextuales y permite interacción por línea de comandos.

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd simpleshop-rag
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

#### Opción 1: Usando pip (tradicional)
```bash
pip install -r requirements.txt
```

#### Opción 2: Usando uv (más rápido)
Si no tienes `uv` instalado, instálalo primero:
```bash
pip install uv
```

Luego instala las dependencias:
```bash
uv pip install -r requirements.txt
```

### 4. Configurar variables de entorno

- Copia el archivo `.env-example` a `.env` y completa los valores necesarios:
  - Claves de API de OpenAI y Langsmith.
  - Rutas a los archivos de datos si necesitas personalizarlas.

```bash
cp .env-example .env
```

---

## ▶️ Ejecución

```bash
python main.py
```

El chatbot se ejecutará en modo CLI. Te pedirá tu nombre de usuario y podrás hacer preguntas sobre productos, tallas, recomendaciones, etc. Para salir, escribe `q`.

---

## 🧠 Lógica de la Aplicación

1. **Identificación del usuario:** El bot solicita el nombre del usuario para buscar su perfil.
2. **Recuperación de contexto:** Utiliza almacenamiento vectorial (FAISS) para buscar información relevante en los perfiles de clientes y el catálogo de productos.
3. **Generación de respuesta:** El LLM (GPT-4o-mini) integra el contexto recuperado y responde de manera personalizada.
4. **Memoria conversacional:** El historial de mensajes se mantiene durante la sesión para dar coherencia a la conversación.

---

## 📁 Estructura de Directorios

```
simpleshop-rag/
│
├── agents/
│   └── profile_lookup_agent.py      # Ejemplo alternativo de agente con Langchain/Langsmith
│
├── data/
│   ├── client_profiles.json         # Perfiles de clientes (JSON)
│   ├── product_catalog.json         # Catálogo de productos (JSON)
│   └── db/                         # Almacenamiento vectorial FAISS
│
├── mappers/
│   ├── profile_mapper.py            # Mapeo y formateo de perfiles de usuario
│   └── product_catalog_mapper.py    # Mapeo y formateo de productos
│
├── tools/
│   └── vector_storage.py            # Funciones para acceso y consulta al vector store
│
├── main.py                         # Script principal del chatbot (CLI)
├── requirements.txt                # Dependencias del proyecto
├── .env-example                    # Ejemplo de configuración de entorno
├── .env                            # Configuración real de entorno (no subir a git)
└── README.md                       # Este archivo