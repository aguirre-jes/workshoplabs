# Comandos de Workshop - Containerización

## Construcción de Imágenes

### Dockerfile Naive
```bash
docker build -t api-status:naive -f Dockerfile.naive .
```

### Dockerfile Producción  
```bash
docker build -t api-status:prod -f Dockerfile.prod .
```

### Buildpack Paketo
```bash
# Instalar pack CLI (macOS)
brew install buildpacks/tap/pack

# Instalar pack CLI (Linux)
curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.33.2/pack-v0.33.2-linux.tgz" | tar -xzf -
sudo mv pack /usr/local/bin/

# Construir con buildpack
pack build api-status:buildpack --builder paketobuildpacks/builder:base
```

## Ejecución de Contenedores

### Ejecutar y auto-eliminar
```bash
docker run --rm -p 8081:8080 --name api-naive api-status:naive
docker run --rm -p 8081:8080 --name api-prod api-status:prod
docker run --rm -p 8081:8080 --name api-buildpack api-status:buildpack
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
```

### Inspeccionar capas
```bash
docker history api-status:naive
docker history api-status:prod
docker history api-status:buildpack
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
```

### Limpieza completa
```bash
docker system prune -f
docker system prune -af  # Incluye imágenes no utilizadas
```

## Azure DevOps

### Configurar variables
```bash
# En Azure DevOps, configurar:
dockerRegistry: 'your-registry.azurecr.io'
imageRepository: 'api-status'
containerRegistry: 'your-acr-connection'
DOCKER_USERNAME: 'service-principal-id'
DOCKER_PASSWORD: 'service-principal-password'
```

### Ejecutar pipelines
- Pipeline Dockerfile: `azure-pipelines-dockerfile.yml`
- Pipeline Buildpack: `azure-pipelines-buildpack.yml`
