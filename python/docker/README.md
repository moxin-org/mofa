# Building and publishing Docker images

Build for both `arm64` and `amd64` platforms at the same time.
You can change `secondstate/gosim-mofa-xlang` to your own account.

```
docker buildx build . --platform linux/arm64,linux/amd64 \
  --tag secondstate/gosim-mofa-xlang:latest -f Dockerfile.multiarch
```

Publish to Docker hub.

```
docker login
docker push secondstate/gosim-mofa-xlang
```
