FROM python:3.13.0-slim-bookworm AS base

ARG service_folder=services/grpc-python-client

WORKDIR app

COPY ./protobufs ./protobufs
COPY ./${service_folder}/requirements.txt ./${service_folder}/

RUN pip install --upgrade pip && \
    pip install -r ./${service_folder}/requirements.txt && \
    python -m grpc_tools.protoc -I ./protobufs --python_out=./${service_folder} --grpc_python_out=./${service_folder} protobufs/ask-random-names.proto

COPY ./${service_folder}/*py ./${service_folder}/

FROM base AS prod

ENV SERVICE_FOLDER=${service_folder}
ENV GRPC_SERVER_FQDN=grpc-python-server
ENV GRPC_SERVER_PORT=50051
CMD exec python ./${SERVICE_FOLDER}/dirty_test.py