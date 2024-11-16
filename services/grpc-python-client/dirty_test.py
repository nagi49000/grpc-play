from time import sleep
import grpc
from ask_random_names_pb2 import RandomNamesRequest
from ask_random_names_pb2_grpc import RandomNamesStub

sleep(1)
channel = grpc.insecure_channel("grpc-python-server:50051")
client = RandomNamesStub(channel)
request = RandomNamesRequest(max_results=5)
print(client.Names(request))
