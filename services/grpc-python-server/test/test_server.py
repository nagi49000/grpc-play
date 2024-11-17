import grpc_testing
import grpc
from google.protobuf.json_format import MessageToDict
import logging
import asyncio
import pytest
from server import RandNameService, get_logger

# imports from auto-generated files
from ask_random_names_pb2_grpc import RandomNamesServicer
import ask_random_names_pb2


@pytest.fixture
def grpc_server():
    logger = get_logger(f"{__name__}-grpc_server")
    rand_name_service = RandNameService(logger, 42)

    # Define a test server. This is defined by a key-value pair of:
    # The .proto service definition. The protobuf which will have been translated into a _pb2.py file, and the service definition is in that file
    # An instance of the class that implements the service definition. This will be related to the service definition, since the class inherits from
    # the Servicer (created in the _pb2_grpc.py file) related to the service definition
    test_server = grpc_testing.server_from_dictionary(
        {
            ask_random_names_pb2.DESCRIPTOR.services_by_name["RandomNames"]: rand_name_service
        },
        grpc_testing.strict_real_time()
    )
    yield test_server


def test_get_logger(caplog):
    logger = get_logger(f"{__name__}-test_get_logger", logging.DEBUG)
    logger.debug("this is a debug message")
    assert "this is a debug message" in caplog.text


def test_random_names_names(grpc_server):
    def get_response_and_code(request):
        # Define a call to the mock server
        # This requires saying which method we are calling calling on the service, by supplying the method definition in the .proto. The
        # protobuf which will have been translated into a _pb2.py file, and the method definition is in the service definition in that file
        # The request also needs to be supplied; the request definition is agin in a .proto file, and translated into a _pb2.py file
        # When invoking the method, one can invoke unary_unary, unary_stream, stream_unary, stream_stream. In this case, the request is simple,
        # with making a single request and getting a single response (like a REST call), so unary_unary is used here
        rpc = grpc_server.invoke_unary_unary(
            ask_random_names_pb2.DESCRIPTOR.services_by_name["RandomNames"].methods_by_name["Names"],
            (),  # docs say this "The RPC’s invocation metadata". No idea what that means.
            request,
            None
        )
        initial_metadata = rpc.initial_metadata()
        response, trailing_metadata, code, details = rpc.termination()
        return response, code

    response, code = get_response_and_code(ask_random_names_pb2.RandomNamesRequest(max_results=5))
    assert code == grpc.StatusCode.OK
    # the service implementation is async, so the response brings back a coroutine (rather than a function) that will give the result
    result = asyncio.run(response)

    assert isinstance(result, ask_random_names_pb2.RandomNamesResponse)
    assert result.IsInitialized()
    assert MessageToDict(result) == {
        "names": [
            "Allison Hill",
            "Noah Rhodes",
            "Angie Henderson",
            "Daniel Wagner",
            "Cristian Santos"
        ]
    }

    response, code = get_response_and_code(ask_random_names_pb2.RandomNamesRequest(max_results=2))
    assert code == grpc.StatusCode.OK
    # the service implementation is async, so the response brings back a coroutine (rather than a function) that will give the result
    result = asyncio.run(response)

    assert isinstance(result, ask_random_names_pb2.RandomNamesResponse)
    assert result.IsInitialized()
    assert MessageToDict(result) == {
        "names": ["Connie Lawrence", "Abigail Shaffer"]
    }


def test_random_names_cities(grpc_server):
    def get_response_and_code(request):
        # Define a call to the mock server
        # This requires saying which method we are calling calling on the service, by supplying the method definition in the .proto. The
        # protobuf which will have been translated into a _pb2.py file, and the method definition is in the service definition in that file
        # The request also needs to be supplied; the request definition is agin in a .proto file, and translated into a _pb2.py file
        # When invoking the method, one can invoke unary_unary, unary_stream, stream_unary, stream_stream. In this case, the request is simple,
        # with making a single request and getting a single response (like a REST call), so unary_unary is used here
        rpc = grpc_server.invoke_unary_unary(
            ask_random_names_pb2.DESCRIPTOR.services_by_name["RandomNames"].methods_by_name["Cities"],
            (),  # docs say this "The RPC’s invocation metadata". No idea what that means.
            request,
            None
        )
        initial_metadata = rpc.initial_metadata()
        response, trailing_metadata, code, details = rpc.termination()
        return response, code

    response, code = get_response_and_code(ask_random_names_pb2.RandomCitiesRequest(max_results=5))
    assert code == grpc.StatusCode.OK
    # the service implementation is async, so the response brings back a coroutine (rather than a function) that will give the result
    result = asyncio.run(response)

    assert isinstance(result, ask_random_names_pb2.RandomCitiesResponse)
    assert result.IsInitialized()
    assert MessageToDict(result) == {
        "cities": [
            "North Judithbury",
            "East Jill",
            "New Roberttown",
            "East Jessetown",
            "Lake Debra"
        ]
    }

    response, code = get_response_and_code(ask_random_names_pb2.RandomCitiesRequest(max_results=2))
    assert code == grpc.StatusCode.OK
    # the service implementation is async, so the response brings back a coroutine (rather than a function) that will give the result
    result = asyncio.run(response)

    assert isinstance(result, ask_random_names_pb2.RandomCitiesResponse)
    assert result.IsInitialized()
    assert MessageToDict(result) == {"cities": ["Robinsonshire", "Lisatown"]}
