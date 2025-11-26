# Examen CI/CD - Murillo 🚀

Proyecto de integración continua y entrega continua (CI/CD) con Flask e IA, diseñado para despliegue automático en VPS mediante GitHub Actions.

## 📋 Descripción

Este proyecto implementa un pipeline CI/CD completo que:

- ✅ Ejecuta pruebas automatizadas con pytest
- ✅ Construye y publica imagen Docker en GitHub Container Registry (GHCR)
- ✅ Despliega automáticamente en VPS mediante Docker Swarm
- ✅ Configura proxy reverso con Traefik
- ✅ Expone la aplicación en `murillo.byronrm.com`

## 🏗️ Estructura del Proyecto

```
├── app.py                          # Aplicación Flask con IA
├── test_app.py                     # Tests automatizados con pytest
├── requirements.txt                # Dependencias de Python
├── Dockerfile                      # Configuración de contenedor
├── Makefile                        # Comandos útiles
├── stack.yml                       # Composición Docker Swarm
├── .github/workflows/ci-cd.yml    # Pipeline de CI/CD
├── .gitignore                      # Archivos ignorados por Git
├── .dockerignore                   # Archivos ignorados por Docker
└── README.md                       # Este archivo
```

## 🚀 Características

### Aplicación Flask
- Endpoint principal `/` que retorna estado y información
- Endpoint `/api/chat` para procesar mensajes con capacidades de IA
- Endpoint `/api/health` para health checks
- Procesamiento de mensajes simple y extensible

### Pipeline CI/CD
- **CI (Continuous Integration):**
  - Descarga el código
  - Configura Python 3.11
  - Instala dependencias
  - Ejecuta tests con pytest

- **CD (Continuous Deployment):**
  - Construye imagen Docker
  - Publica en GHCR con tag `murillo:1.0.5`
  - Transfiere `stack.yml` a VPS
  - Despliega automáticamente con Docker Swarm
  - Verifica estado del despliegue

## 🛠️ Instalación Local

### Requisitos
- Python 3.11+
- Docker y Docker Compose
- Git

### Pasos

1. **Clonar el repositorio:**
```bash
git clone <repositorio>
cd Examen-2do-P
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🧪 Tests

### Ejecutar tests localmente:
```bash
pytest test_app.py -v
```

### Tests incluidos:
- ✅ Home endpoint
- ✅ Health check
- ✅ Chat endpoint con mensaje válido
- ✅ Chat endpoint sin mensaje
- ✅ Procesamiento de IA

## 🐳 Docker

### Construir imagen:
```bash
make docker-build
```

### Ejecutar contenedor:
```bash
make docker-run
```

### Detener contenedor:
```bash
docker stop murillo
docker rm murillo
```

## 📦 Makefile Comandos

```bash
make build          # Instalar dependencias
make run            # Ejecutar aplicación
make docker-build   # Construir imagen Docker
make docker-run     # Ejecutar contenedor
```

## 🔐 Secretos de GitHub Actions

Configurar en `Settings > Secrets and variables > Actions`:

- `VPS_HOST` - IP o dominio del VPS
- `VPS_USER` - Usuario SSH del VPS
- `VPS_PASSWORD` - Contraseña SSH
- `VPS_SSH_PORT` - Puerto SSH (defecto: 22)

## 🌐 Despliegue

### En VPS:

1. **Configurar Traefik:**
```bash
docker network create traefik-public
```

2. **Desplegar Traefik:**
```bash
docker stack deploy -c traefik-stack.yml traefik
```

3. **El pipeline despliega automáticamente:**
- Cuando hay push a `main`
- La imagen se publica en GHCR
- Se actualiza automáticamente en el VPS

### Acceso:
- URL: `https://murillo.byronrm.com`
- Health: `https://murillo.byronrm.com/api/health`
- Chat: `POST https://murillo.byronrm.com/api/chat`

## 📝 Uso de la API

### 1. Health Check
```bash
curl https://murillo.byronrm.com/api/health
```

**Respuesta:**
```json
{
  "status": "healthy"
}
```

### 2. Endpoint Principal
```bash
curl https://murillo.byronrm.com/
```

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Saludos a todos desde Python con IA",
  "version": "1.0.5"
}
```

### 3. Chat con IA
```bash
curl -X POST https://murillo.byronrm.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hola"}'
```

**Respuesta:**
```json
{
  "status": "ok",
  "input": "hola",
  "response": "¡Hola! ¿Cómo estás?"
}
```

## 📊 Versionado

- **Versión actual:** 1.0.5
- **Imagen Docker:** `ghcr.io/byronmoreno/murillo:1.0.5`
- **Subdominio:** `murillo.byronrm.com`

## 🔄 Flujo de Git

1. Crear rama de desarrollo
2. Hacer cambios y commits organizados
3. Push a rama principal (`main`)
4. GitHub Actions dispara el pipeline
5. Tests se ejecutan
6. Imagen se construye y publica
7. Despliegue automático en VPS

## ⚠️ Notas Importantes

- El pipeline solo despliega en push a `main`
- Los tests deben pasar para que el build continúe
- La imagen se etiqueta automáticamente con `1.0.5` y `latest`
- El despliegue es completamente automático sin intervención manual

## 📝 Licencia

MIT

## 👤 Autor

Murillo - Examen CI/CD 2do Parcial
