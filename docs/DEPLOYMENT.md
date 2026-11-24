# 部署

## Docker

```bash
docker build -t arbiter .
docker run -p 8000:8000 arbiter
```

## docker-compose

```bash
docker compose up -d
```

## Kubernetes / Helm

```bash
helm install arbiter ./helm
kubectl apply -f k8s/
```
