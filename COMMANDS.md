# Comandos de Workshop - Containerización

## DevContainer (Recomendado)

### Usar DevContainer en VS Code
```bash
# 1. Abrir proyecto en VS Code
code .

# 2. Instalar extensión "Dev Containers" si no está instalada
# 3. Presionar Ctrl+Shift+P
# 4. Seleccionar "Dev Containers: Reopen in Container"
# 5. Esperar a que se construya el contenedor

# Verificar herramientas pre-instaladas
docker --version
pack --version
python --version
curl --version
jq --version
```

### Ventajas del DevContainer
- ✅ Todas las herramientas pre-instaladas
- ✅ Docker-in-Docker habilitado
- ✅ Configuración consistente en todo el equipo
- ✅ Sin contaminar el sistema host
- ✅ Extensiones VS Code incluidas

## Construcción de Imágenes

### Dockerfile Naive
```bash
docker build -t api-status:naive -f Dockerfile.naive .
```

### Dockerfile Producción  
```bash
docker build -t api-status:prod -f Dockerfile.prod .
```

### Golden Image (Imagen Base Corporativa)
```bash
# 1. Construir la Golden Image (base corporativa)
docker build -t mi-empresa/base-alpine:1.0 -f Dockerfile.base .

# 2. Construir aplicación usando Golden Image
docker build -t api-status:golden -f Dockerfile.golden .

# 3. Publicar Golden Image en ACR (una sola vez)
docker tag mi-empresa/base-alpine:1.0 acrworkshopcontainers2024.azurecr.io/mi-empresa/base-alpine:1.0
docker push acrworkshopcontainers2024.azurecr.io/mi-empresa/base-alpine:1.0

# 4. Versionado de Golden Images
docker build -t mi-empresa/base-alpine:1.0.0 -f Dockerfile.base .
docker tag mi-empresa/base-alpine:1.0.0 mi-empresa/base-alpine:latest
docker tag mi-empresa/base-alpine:1.0.0 mi-empresa/base-alpine:stable
```

### Buildpack Paketo
```bash
# Instalar pack CLI (Linux)
curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.33.2/pack-v0.33.2-linux.tgz" | tar -xzf -
sudo mv pack /usr/local/bin/
pack version

# Si usas DevContainer, pack ya está pre-instalado
pack version  # Verificar instalación

# Construir con buildpack
pack build api-status:buildpack --builder paketobuildpacks/builder:base
```

## Ejecución de Contenedores

### Ejecutar y auto-eliminar
```bash
docker run --rm -p 8081:8080 --name api-naive api-status:naive
docker run --rm -p 8081:8080 --name api-prod api-status:prod
docker run --rm -p 8081:8080 --name api-buildpack api-status:buildpack
docker run --rm -p 8081:8080 --name api-golden api-status:golden
```

### Ejecutar en background
```bash
docker run -d -p 8081:8080 --name api-prod api-status:prod
```

## Pruebas de API

### Endpoints básicos
```bash
curl http://localhost:8081/
curl http://localhost:8081/status  
curl http://localhost:8081/hostname
```

### Con formato JSON
```bash
curl -s http://localhost:8081/ | python -m json.tool
curl -s http://localhost:8081/status | python -m json.tool
curl -s http://localhost:8081/hostname | python -m json.tool
```

### Con headers
```bash
curl -i http://localhost:8081/
curl -i http://localhost:8081/status
curl -i http://localhost:8081/hostname
```

## Análisis de Imágenes

### Comparar tamaños
```bash
docker images | grep api-status
docker images | grep mi-empresa  # Ver Golden Images
```

### Inspeccionar capas
```bash
docker history api-status:naive
docker history api-status:prod
docker history api-status:buildpack
docker history api-status:golden
docker history mi-empresa/base-alpine:1.0  # Golden Image base
```

### Análisis detallado
```bash
docker inspect api-status:prod
```

## Gestión de Contenedores

### Ver contenedores activos
```bash
docker ps
```

### Ver logs
```bash
docker logs api-prod
```

### Acceder al contenedor
```bash
docker exec -it api-prod /bin/bash
```

### Parar contenedores
```bash
docker stop api-prod
docker stop $(docker ps -q)  # Parar todos
```

## Limpieza

### Eliminar contenedores
```bash
docker rm api-prod
docker rm $(docker ps -aq)  # Eliminar todos
```

### Eliminar imágenes
```bash
docker rmi api-status:naive
docker rmi api-status:prod  
docker rmi api-status:buildpack
docker rmi api-status:golden
docker rmi mi-empresa/base-alpine:1.0  # Golden Image base
```

### Limpieza completa
```bash
docker system prune -f
docker system prune -af  # Incluye imágenes no utilizadas
```

## GitHub Actions

### Configurar secrets en GitHub
```bash
# En GitHub: Settings → Secrets and variables → Actions
# Agregar Repository secrets:
ACR_USERNAME: 'acrworkshopcontainers2024'
ACR_PASSWORD: 'tu-password-de-acr'
```

### Ejecución manual de workflows
```bash
# 1. Ve a tu repositorio en GitHub
# 2. Actions → Selecciona workflow
# 3. "Run workflow" → Configura opciones
# 4. "Run workflow"

# Workflow: "Docker Build and Test"
# Opciones: both, naive, production

# Workflow: "Buildpack Build and Test" 
# Opciones environment: both, development, production
# Opción builder: paketobuildpacks/builder-jammy-base
```

### Triggers automáticos
```bash
# Docker Build workflow se ejecuta al modificar:
- Dockerfile.*
- requirements.txt  
- app.py

# Buildpack Build workflow se ejecuta al modificar:
- requirements.txt
- app.py
- .python-version
```

### Ver resultados
```bash
# Imágenes generadas en ACR:
# Docker workflow:
acrworkshopcontainers2024.azurecr.io/api-status:{run_id}-naive
acrworkshopcontainers2024.azurecr.io/api-status:latest-naive
acrworkshopcontainers2024.azurecr.io/api-status:{run_id}-prod  
acrworkshopcontainers2024.azurecr.io/api-status:latest-prod

# Buildpack workflow:
acrworkshopcontainers2024.azurecr.io/api-status:{run_id}-dev
acrworkshopcontainers2024.azurecr.io/api-status:{run_id}-prod
```
