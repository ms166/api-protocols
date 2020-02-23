import grpc

import prime_api_pb2
import prime_api_pb2_grpc

channel = grpc.insecure_channel('localhost:6000')

stub = prime_api_pb2_grpc.PrimeServiceStub(channel)

n = prime_api_pb2.Request(n=16)

response = stub.get_primes(n)

print(response.primes)
