# Workshop: Containerización de Aplicaciones Python

Este workshop te guía a través de diferentes estrategias de containerización para una aplicación Flask simple, mostrando desde enfoques básicos hasta técnicas avanzadas de producción.

## 📋 Contenido del Workshop

- [Aplicación de Ejemplo](#aplicación-de-ejemplo)
- [Dockerfiles: Naive vs Producción](#dockerfiles-naive-vs-producción)
- [Buildpacks con Paketo](#buildpacks-con-paketo)
- [Pipelines de Azure DevOps](#pipelines-de-azure-devops)
- [Comandos Útiles](#comandos-útiles)

## 🚀 Aplicación de Ejemplo

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

## 🐳 Dockerfiles: Naive vs Producción

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

## 📦 Buildpacks con Paketo

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

## ⚙️ Pipelines de Azure DevOps

### Pipeline 1: Construcción con Dockerfile

Crea un archivo `azure-pipelines-dockerfile.yml`:

```yaml
trigger:
- main

variables:
  dockerRegistry: 'your-registry.azurecr.io'
  imageRepository: 'api-status'
  containerRegistry: 'your-acr-connection'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile.prod'
  tag: '$(Build.BuildId)'

stages:
- stage: Build
  displayName: Build and push stage
  jobs:
  - job: Build
    displayName: Build
    pool:
      vmImage: ubuntu-latest
    steps:
    - task: Docker@2
      displayName: Build and push Docker image (Naive)
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(Build.SourcesDirectory)/Dockerfile.naive
        containerRegistry: $(containerRegistry)
        tags: |
          $(tag)-naive
          latest-naive

    - task: Docker@2
      displayName: Build and push Docker image (Production)
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(Build.SourcesDirectory)/Dockerfile.prod
        containerRegistry: $(containerRegistry)
        tags: |
          $(tag)-prod
          latest-prod

    - task: Docker@2
      displayName: Display image sizes
      inputs:
        command: run
        arguments: '--rm docker images | grep api-status'
```

### Pipeline 2: Construcción con Buildpack

Crea un archivo `azure-pipelines-buildpack.yml`:

```yaml
trigger:
- main

variables:
  dockerRegistry: 'your-registry.azurecr.io'
  imageRepository: 'api-status'
  containerRegistry: 'your-acr-connection'
  tag: '$(Build.BuildId)'

stages:
- stage: BuildWithBuildpack
  displayName: Build with Paketo Buildpack
  jobs:
  - job: BuildPack
    displayName: Build with Pack CLI
    pool:
      vmImage: ubuntu-latest
    steps:
    - script: |
        # Instalar pack CLI
        curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.33.2/pack-v0.33.2-linux.tgz" | tar -xzf -
        sudo mv pack /usr/local/bin/
        pack version
      displayName: 'Install Pack CLI'

    - script: |
        # Construir imagen con buildpack
        pack build $(dockerRegistry)/$(imageRepository):$(tag)-buildpack \
          --builder paketobuildpacks/builder:base \
          --publish
      displayName: 'Build and publish with Buildpack'

    - script: |
        # Tag como latest
        docker tag $(dockerRegistry)/$(imageRepository):$(tag)-buildpack \
                   $(dockerRegistry)/$(imageRepository):latest-buildpack
        docker push $(dockerRegistry)/$(imageRepository):latest-buildpack
      displayName: 'Tag and push latest'
```

## 🔧 Comandos Útiles

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
   - Pipelines de Azure DevOps
   - Integración con registros de contenedores

4. **Optimización de imágenes**
   - Cache de capas de Docker
   - Reducción de tamaño de imagen

## 📚 Recursos Adicionales

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Paketo Buildpacks](https://paketo.io/)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)

---

**¡Feliz containerización! 🐳**