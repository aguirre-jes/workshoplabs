# Workshop: Containerización de Aplicaciones Python

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
```bash
pip install -r requirements.txt
python app.py
```

### Probar la API
```bash
curl http://localhost:8080/
curl http://localhost:8080/status
curl http://localhost:8080/hostname
```

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

## Buildpacks con Paketo

Los buildpacks detectan automáticamente el lenguaje y crean imágenes optimizadas sin necesidad de Dockerfiles.

### Prerequisitos
```bash
# Instalar pack CLI
brew install buildpacks/tap/pack
# o
(curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.33.2/pack-v0.33.2-macos.tgz" | tar -xzf -) && mv pack /usr/local/bin/
```

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