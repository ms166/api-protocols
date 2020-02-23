import prime_api_pb2
import prime_api_pb2_grpc

import grpc
from concurrent import futures
import time

class MyPrimeService(prime_api_pb2_grpc.PrimeServiceServicer):
    MAX = int(1e3 + 1)
    primes = []

    def calc_primes():
        is_prime = [True for x in range(0, MyPrimeService.MAX)]
        is_prime[0] = is_prime[1] = False
        for i in range(2, MyPrimeService.MAX):
            if(is_prime[i]):
                for j in range(i * i, MyPrimeService.MAX, i):
                    is_prime[j] = False
                MyPrimeService.primes.append(i)

    def get_primes(self, request, context):
        MyPrimeService.calc_primes()
        n = request.n
        response = prime_api_pb2.Response()
        response.primes.extend(MyPrimeService.primes[:n])
        return response

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prime_api_pb2_grpc.add_PrimeServiceServicer_to_server(MyPrimeService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    print("Listening on port {}..".format(port))
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__== "__main__":
    serve(6000)


