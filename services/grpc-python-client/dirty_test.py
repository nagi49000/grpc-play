from os import getenv
from time import sleep
import grpc
from ask_random_names_pb2 import RandomNamesRequest, RandomCitiesRequest
from ask_random_names_pb2_grpc import RandomNamesStub

sleep(1)
channel = grpc.insecure_channel(f"{getenv('GRPC_SERVER_FQDN', 'localhost')}:{getenv('GRPC_SERVER_PORT', '50051')}")
client = RandomNamesStub(channel)

request = RandomNamesRequest(max_results=5)
print(client.Names(request))

request = RandomCitiesRequest(max_results=6)
print(client.Cities(request))

nginx_server = getenv("NGINX_GRPC_GATEWAY_FQDN", None)
nginx_port = getenv("NGINX_GRPC_GATEWAY_PORT", None)
if nginx_server and nginx_port:
    channel = grpc.insecure_channel(f"{nginx_server}:{nginx_port}")
    client = RandomNamesStub(channel)
    request = RandomNamesRequest(max_results=2)
    print(client.Names(request))
