# Wo## 📋 Contenido del Workshop

- [Aplicacion de Ejemplo](#aplicacion-de-ejemplo)
- [Entorno de Desarrollo con DevContainers](#entorno-de-desarrollo-con-devcontainers)
- [Dockerfiles: Naive vs Produccion](#dockerfiles-naive-vs-produccion)
- [Golden Images: Proceso en Dos Etapas](#golden-images-proceso-en-dos-etapas)
- [Buildpacks con Paketo](#buildpacks-con-paketo)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Comandos utiles](#comandos-utiles) Containerización de Aplicaciones Python

Este workshop te guía a través de diferentes estrategias de containerización para una aplicación Flask simple, mostrando desde enfoques básicos hasta técnicas avanzadas de producción.

## 📋 Contenido del Workshop

- [Aplicacion de Ejemplo](#aplicacion-de-ejemplo)
- [Dockerfiles: Naive vs Producción](#dockerfiles-naive-vs-produccion)
- [Buildpacks con Paketo](#buildpacks-con-paketo)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Comandos utiles](#comandos-utiles)
- [Referencia Completa de Comandos](COMMANDS.md)

## 🚀 aplicacion de ejemplo

Nuestra aplicación Flask (`app.py`) expone tres endpoints:

- **`/`** - Mensaje de bienvenida
- **`/status`** - Estado del servidor y timestamp
- **`/hostname`** - Hostname del contenedor (útil para demostrar aislamiento)

### Ejecutar localmente

**Opción 1: Desarrollo local tradicional**
```bash
pip install -r requirements.txt
python app.py
```

**Opción 2: Usando DevContainer (Recomendado)**
Este repositorio incluye un DevContainer configurado con todas las herramientas necesarias.

1. Abre el proyecto en VS Code
2. Instala la extensión "Dev Containers"
3. Presiona `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
4. El contenedor incluye Docker, pack CLI y todas las herramientas pre-instaladas

### Probar la API
```bash
curl http://localhost:8080/
curl http://localhost:8080/status
curl http://localhost:8080/hostname
```

## 🐳 Entorno de Desarrollo con DevContainers

Este repositorio incluye una configuración completa de **DevContainer** que proporciona un entorno de desarrollo consistente y reproducible.

### ¿Qué es un DevContainer?

Un DevContainer es un contenedor Docker completamente configurado que incluye:
- ✅ Runtime de la aplicación (Python)
- ✅ Docker-in-Docker para construir imágenes
- ✅ Pack CLI para Buildpacks
- ✅ Extensiones de VS Code pre-configuradas
- ✅ Herramientas de desarrollo (git, curl, jq)

### Cómo usar el DevContainer

**Prerequisitos:**
- VS Code instalado
- Extensión "Dev Containers" instalada
- Docker ejecutándose en tu máquina

**Pasos:**
1. Clona este repositorio
2. Abre el proyecto en VS Code
3. Presiona `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
4. Selecciona **"Dev Containers: Reopen in Container"**
5. Espera a que el contenedor se construya (solo la primera vez)
6. ¡Listo! Todas las herramientas están disponibles

### Herramientas Pre-instaladas en el DevContainer

```bash
# Verificar herramientas disponibles
docker --version          # Docker para construir imágenes
pack --version            # Pack CLI para Buildpacks
python --version          # Python runtime
git --version             # Control de versiones
curl --version            # Testing de APIs
jq --version              # Procesamiento JSON
```

### Extensiones VS Code Incluidas

- **GitHub Actions**: Edición y validación de workflows
- **YAML/XML**: Soporte para archivos de configuración
- **Markdown Lint**: Validación de documentación
- **SonarLint**: Análisis de calidad de código
- **GitHub Copilot**: Asistente de codificación IA
- **Code Spell Checker**: Corrector ortográfico

### Ventajas del DevContainer

| Aspecto | Sin DevContainer | Con DevContainer |
|---------|------------------|------------------|
| **Configuración** | Manual en cada máquina | Automática e idéntica |
| **Dependencias** | Instalación manual | Pre-instaladas |
| **Versiones** | Pueden diferir entre devs | Consistentes para todo el equipo |
| **Onboarding** | Horas de configuración | Minutos |
| **Aislamiento** | Contamina el sistema host | Entorno limpio y aislado |

## Dockerfiles: Naive vs Produccion

### 1. Dockerfile Naive (`Dockerfile.naive`)

**Características:**
- ✅ Simple y directo
- ❌ No optimizado para cache
- ❌ Corre como root (inseguro)
- ❌ Imagen más grande

```bash
# Construir imagen naive
docker build -t api-status:naive -f Dockerfile.naive .

# Ejecutar contenedor
docker run --rm -p 8081:8080 --name api-naive-container api-status:naive
```

### 2. Dockerfile Producción (`Dockerfile.prod`)

**Características:**
- ✅ Multi-stage build (imagen más pequeña)
- ✅ Optimización de cache de Docker
- ✅ Usuario sin privilegios (seguridad)
- ✅ Principio de mínimo privilegio

```bash
# Construir imagen de producción
docker build -t api-status:prod -f Dockerfile.prod .

# Ejecutar contenedor
docker run --rm -p 8081:8080 --name api-prod-container api-status:prod
```

### Comparación de Tamaños
```bash
docker images | grep api-status
```

## 🏢 Golden Images: Proceso en Dos Etapas

Una estrategia empresarial avanzada para estandarizar y asegurar las imágenes base en toda la organización.

### ¿Qué es una Golden Image?

Una **Golden Image** es una imagen base corporativa personalizada que sirve como punto de partida estandarizado y seguro para todos los proyectos de la empresa. En lugar de que cada equipo parta de imágenes públicas diferentes, todos utilizan la misma base controlada y auditada.

### El Proceso en Dos Etapas

#### **Etapa 1: Crear tu Imagen Base Corporativa**

En esta etapa, no estás construyendo tu aplicación final. Estás creando una nueva imagen base que servirá como el punto de partida estandarizado para todos los proyectos.

**El "Porqué":**

- **🔒 Seguridad**: Instalas y configuras herramientas de seguridad o certificados de confianza una sola vez
- **📏 Estándares**: Incluyes utilidades comunes (curl, jq, git) que todos los equipos necesitarán
- **📦 Dependencias Comunes**: Pre-instalas librerías o paquetes base requeridos por la organización
- **🚀 Velocidad**: Los equipos ya no tienen que "reinventar la rueda" en cada Dockerfile

#### **Etapa 2: Construir la Aplicación Final**

El Dockerfile de tu aplicación se vuelve mucho más simple y limpio, porque parte de tu base personalizada.

### Implementación Práctica

#### Dockerfile.base (Golden Image)

```dockerfile
# Partimos de una imagen pública, oficial y ligera como Alpine
FROM alpine:3.20

# Etiquetamos la imagen para identificar al responsable y la versión
LABEL maintainer="equipo.devops@miempresa.com"
LABEL version="1.0"
LABEL description="Golden Image corporativa basada en Alpine"

# Instalamos nuestras herramientas base estándar y actualizamos los certificados
RUN apk add --no-cache \
    bash \
    curl \
    jq \
    git \
    ca-certificates \
    tzdata \
    && update-ca-certificates

# Configuramos zona horaria corporativa
ENV TZ=America/Mexico_City

# Creamos usuario estándar para aplicaciones
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

# Esta imagen no se ejecuta sola, solo sirve como base.
# Por eso no tiene un comando CMD.
```

#### Dockerfile.golden (Aplicación con Golden Image)

```dockerfile
# ¡LA LÍNEA CLAVE!
# Ya no partimos de "alpine", sino de NUESTRA "Golden Image".
FROM mi-empresa/base-alpine:1.0

WORKDIR /app

# Cambiar al usuario estándar (ya viene configurado en la Golden Image)
USER appuser

# ---- El resto de la lógica sigue aquí ----
# ¡Ya no necesitas instalar curl, jq o bash, ya vienen en la base!
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

EXPOSE 8080

CMD ["python", "app.py"]
```

### Comandos de Construcción

```bash
# 1. Construir la Golden Image (una sola vez)
docker build -t mi-empresa/base-alpine:1.0 -f Dockerfile.base .

# 2. Publicar en tu registro interno
docker tag mi-empresa/base-alpine:1.0 acrworkshopcontainers2024.azurecr.io/mi-empresa/base-alpine:1.0
docker push acrworkshopcontainers2024.azurecr.io/mi-empresa/base-alpine:1.0

# 3. Construir aplicación usando la Golden Image
docker build -t api-status:golden -f Dockerfile.golden .
```

### Beneficios del Enfoque Golden Image

| Aspecto | Sin Golden Image | Con Golden Image |
|---------|------------------|------------------|
| **Seguridad** | Cada equipo maneja su propia seguridad | Seguridad centralizada y auditada |
| **Consistencia** | Diferentes bases, diferentes comportamientos | Base única, comportamiento predecible |
| **Velocidad** | Reinstalar utilidades en cada build | Utilidades pre-instaladas |
| **Mantenimiento** | Actualizaciones dispersas | Actualización centralizada |
| **Compliance** | Difícil de auditar | Fácil auditoría y control |

### Gestión y Versionado

```bash
# Versionado semántico de Golden Images
docker build -t mi-empresa/base-alpine:1.0.0 -f Dockerfile.base .
docker build -t mi-empresa/base-alpine:1.0.1 -f Dockerfile.base .  # Parche
docker build -t mi-empresa/base-alpine:1.1.0 -f Dockerfile.base .  # Mejora menor

# Tags para diferentes ambientes
docker tag mi-empresa/base-alpine:1.0.0 mi-empresa/base-alpine:latest
docker tag mi-empresa/base-alpine:1.0.0 mi-empresa/base-alpine:stable
```

### Mejores Prácticas

1. **📅 Actualización Regular**: Programa builds automáticos de la Golden Image para parches de seguridad
2. **🧪 Testing**: Prueba exhaustivamente la Golden Image antes de publicar nuevas versiones
3. **📚 Documentación**: Mantén documentado qué contiene cada versión de la Golden Image
4. **🔄 Migración Gradual**: Permite que los equipos migren gradualmente a nuevas versiones
5. **📊 Monitoreo**: Rastrea qué equipos usan qué versiones de la Golden Image

## Buildpacks con Paketo

Los buildpacks detectan automáticamente el lenguaje y crean imágenes optimizadas sin necesidad de Dockerfiles.

### Prerequisitos

**Instalación de pack CLI (Linux)**

```bash
# Instalar pack CLI en Linux
curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.33.2/pack-v0.33.2-linux.tgz" | tar -xzf -
sudo mv pack /usr/local/bin/
pack version
```

**💡 Usando DevContainer (Recomendado):**
Si usas el DevContainer incluido en este repositorio, pack CLI ya está pre-instalado junto con Docker y todas las herramientas necesarias.

### Construcción con Paketo
```bash
# Construir imagen con buildpack
pack build api-status:buildpack --builder paketobuildpacks/builder:base

# Ejecutar contenedor
docker run --rm -p 8081:8080 --name api-buildpack-container api-status:buildpack
```

### Ventajas de Buildpacks
- 🔄 Actualizaciones automáticas de seguridad
- 📦 Detección automática de dependencias
- 🎯 Optimización automática para el runtime
- 🔧 Sin necesidad de mantener Dockerfiles

## GitHub Actions Workflows

Este workshop incluye dos workflows de GitHub Actions para automatizar la construcción y publicación de imágenes:

### Workflow 1: Docker Build (`.github/workflows/docker-build.yaml`)

**Triggers automáticos:**
- Push o PR cuando se modifiquen: `Dockerfile.*`, `requirements.txt`, `app.py`

**Ejecución manual:**
- Desde Actions → "Docker Build and Test" → "Run workflow"
- Opciones: `both`, `naive`, `production`

**Características:**
- ✅ Construye imágenes con Dockerfiles
- ✅ Publica a Azure Container Registry
- ✅ Tags: `{run_id}-naive`, `{run_id}-prod`, `latest-naive`, `latest-prod`
- ✅ Tests automáticos de endpoints

```yaml
name: Docker Build and Test

on:
  push:
    branches: [ main ]
    paths:
      - 'Dockerfile.*'
      - 'requirements.txt'
      - 'app.py'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to build'
        required: true
        default: 'both'
        type: choice
        options:
        - both
        - naive
        - production

env:
  REGISTRY: acrworkshopcontainers2024.azurecr.io
  IMAGE_NAME: api-status
```

### Workflow 2: Buildpack Build (`.github/workflows/buildpack-build.yaml`)

**Triggers automáticos:**
- Push cuando se modifiquen: `requirements.txt`, `app.py`, `.python-version`

**Ejecución manual:**
- Desde Actions → "Buildpack Build and Test" → "Run workflow"
- Opciones de environment: `both`, `development`, `production`
- Opción de builder: Permite especificar buildpack diferente

**Características:**
- ✅ Construye imágenes con Paketo Buildpacks
- ✅ Sin necesidad de Dockerfiles
- ✅ Tags: `{run_id}-dev`, `{run_id}-prod`
- ✅ Inspección automática de metadata de buildpacks

```yaml
name: Buildpack Build and Test

on:
  push:
    branches: [ main ]
    paths:
      - 'requirements.txt'
      - 'app.py'
      - '.python-version'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to build'
        required: true
        default: 'both'
        type: choice
        options:
        - both
        - development
        - production
      builder:
        description: 'Buildpack builder to use'
        required: false
        default: 'paketobuildpacks/builder-jammy-base'
        type: string
```

### Configuración de Secrets

Para que los workflows funcionen, configura estos secrets en GitHub:

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Agrega los siguientes Repository secrets:
   - `ACR_USERNAME`: Usuario de Azure Container Registry
   - `ACR_PASSWORD`: Contraseña de Azure Container Registry

### Cómo ejecutar workflows manualmente

1. **Ve a tu repositorio en GitHub**
2. **Actions** → Selecciona el workflow
3. **"Run workflow"** → Configura opciones
4. **"Run workflow"** para ejecutar

### Comparación de Workflows

| Característica | Docker Build | Buildpack Build |
|---|---|---|
| **Trigger** | Cambios en Dockerfiles | Cambios en código Python |
| **Método** | Dockerfiles tradicionales | Cloud Native Buildpacks |
| **Configuración** | Manual en Dockerfile | Automática por detección |
| **Seguridad** | Depende del Dockerfile | Imágenes base mantenidas |
| **Tamaño** | Variable | Optimizado automáticamente |
| **Mantenimiento** | Manual | Automático |

## Comandos utiles

### Construcción Local
```bash
# Construir todas las variantes
docker build -t api-status:naive -f Dockerfile.naive .
docker build -t api-status:prod -f Dockerfile.prod .
pack build api-status:buildpack --builder paketobuildpacks/builder:base

# Comparar tamaños
docker images | grep api-status
```

### Ejecución y Pruebas
```bash
# Ejecutar (auto-remove al parar)
docker run --rm -p 8081:8080 --name api-test api-status:prod

# Probar endpoints
curl http://localhost:8081/
curl http://localhost:8081/status
curl http://localhost:8081/hostname

# Ver logs
docker logs api-test

# Inspeccionar contenedor
docker exec -it api-test /bin/bash
```

### Limpieza
```bash
# Parar todos los contenedores
docker stop $(docker ps -q)

# Limpiar imágenes no utilizadas
docker system prune -f

# Remover imágenes específicas
docker rmi api-status:naive api-status:prod api-status:buildpack
```

## 🎯 Objetivos de Aprendizaje

Al completar este workshop habrás aprendido:

1. **Diferencias entre enfoques de containerización**
   - Dockerfile simple vs optimizado
   - Buildpacks vs Dockerfiles tradicionales

2. **Mejores prácticas de seguridad**
   - Usuarios sin privilegios
   - Multi-stage builds
   - Minimización de superficie de ataque

3. **Automatización con CI/CD**
   - GitHub Actions workflows
   - Integración con Azure Container Registry
   - Ejecución automática y manual de pipelines

4. **Optimización de imágenes**
   - Cache de capas de Docker
   - Reducción de tamaño de imagen

## 📚 Recursos Adicionales

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Paketo Buildpacks](https://paketo.io/)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## ¡Feliz containerización! 🐳