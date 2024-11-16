# grpc-play
A play area for building gRPC services

### autogenerating gRPC code from .proto files

In the root of the repo, run
```
python -m grpc_tools.protoc -I ./protobufs --python_out=services/grpc-python-server/ --grpc_python_out=services/grpc-python-server/ protobufs/ask-random-names.proto
python -m grpc_tools.protoc -I ./protobufs --python_out=services/grpc-python-client/ --grpc_python_out=services/grpc-python-client/ protobufs/ask-random-names.proto
```

### docker implementation

A server and test client can be brought up using the docker-compose in the root of the repo
```
docker compose up --build
```