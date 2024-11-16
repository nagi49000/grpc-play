# grpc-play
play area for building gRPC services

### autogenerating gprc code

Navigate to `services/grpc-python-server/` and run
```
python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/ask-random-names.proto
```
