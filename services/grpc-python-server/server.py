import asyncio
import grpc
import logging
from faker import Faker
from signal import signal, SIGTERM
# imports from auto-generated files
from ask_random_names_pb2_grpc import RandomNamesServicer, add_RandomNamesServicer_to_server
from ask_random_names_pb2 import RandomNamesResponse, RandomNamesRequest


def get_logger(log_name: str, log_level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(log_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger


class RandNameService(RandomNamesServicer):

    def __init__(self, logger: logging.Logger, faker_seed: int | None = None):
        self._logger = logger
        self._fake = Faker()
        Faker.seed(faker_seed)

    async def Names(
            self,
            request: RandomNamesRequest,
            context: grpc._cython.cygrpc._SyncServicerContext
    ) -> RandomNamesResponse:
        self._logger.debug(f"RandNameService.Names received request {request}")
        fake_names = [self._fake.name() for _ in range(request.max_results)]
        return RandomNamesResponse(names=fake_names)


async def serve(port: int = 50051, faker_seed: int | None = None):
    logger = get_logger("grpc-python-server", logging.DEBUG)
    server = grpc.aio.server()
    add_RandomNamesServicer_to_server(RandNameService(logger), server)
    server.add_insecure_port(f"0.0.0.0:{port}")
    await server.start()
    logger.info(f"gRPC python server started on port {port}")

    def handle_sigterm(*_):
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)

    signal(SIGTERM, handle_sigterm)
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(serve())
