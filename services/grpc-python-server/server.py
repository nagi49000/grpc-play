import asyncio
import grpc
from faker import Faker
# imports from auto-generated files
from ask_random_names_pb2_grpc import RandomNamesServicer, add_RandomNamesServicer_to_server
from ask_random_names_pb2 import RandomNamesResponse


fake = Faker()
Faker.seed(0)


class RandNameService(RandomNamesServicer):
    def Names(self, request, context):
        fake_names = [fake.name() for _ in range(request.max_results)]
        return RandomNamesResponse(names=fake_names)


async def serve():
    server = grpc.aio.server()
    add_RandomNamesServicer_to_server(RandNameService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    print("HOLA")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(serve())
