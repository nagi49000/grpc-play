FROM python:3.13.0-slim-bookworm AS base

ARG service_folder=services/grpc-python-server

WORKDIR app

COPY ./protobufs ./protobufs
COPY ./${service_folder}/requirements.txt ./${service_folder}/

RUN pip install --upgrade pip && \
    pip install -r ./${service_folder}/requirements.txt && \
    python -m grpc_tools.protoc -I ./protobufs --python_out=./${service_folder} --grpc_python_out=./${service_folder} protobufs/ask-random-names.proto

COPY ./${service_folder}/*py ./${service_folder}/

FROM base AS tester

COPY ./${service_folder}/requirements-test.txt ./${service_folder}/
COPY ./${service_folder}/test ./${service_folder}/test

RUN cd ${service_folder} && \
    pip install -r requirements-test.txt && \
    python -m pytest --cov=./

FROM base AS prod

ENV SERVICE_FOLDER=${service_folder}
CMD exec python ./${SERVICE_FOLDER}/server.py