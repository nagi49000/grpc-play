import asyncio
import grpc


async def serve():
    server = grpc.aio.server()
    server.add_insecure_port("0.0.0.0:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(serve())
