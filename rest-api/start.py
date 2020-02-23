from flask import Flask, jsonify, request, make_response, abort
app = Flask(__name__)

MAX = int(1e3 + 1)
calculated = False

primes = []
def calc_primes():
    global primes
    is_prime = [True for x in range(0, MAX)]
    is_prime[0] = is_prime[1] = False
    for i in range(2, MAX):
        if(is_prime[i]):
            for j in range(i * i, MAX, i):
                is_prime[j] = False
            primes.append(i)
    global calculated
    calculated = True


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)



@app.route('/primes', methods=['GET'])
def get_primes():
    print(request.json)
    if(calculated == False):
        calc_primes()
    if(len(request.args) == 0):
        return jsonify(primes[:1000])
    if('n' in request.args):
        n = int(request.args['n'])
        if(n < 1 or n > len(primes)):
            abort(400)
        return jsonify(primes[:n])
    else:
        abort(400)

def check_if_prime(n):
    for prime in primes:
        if(prime * prime > n):
            return True
        if(n % prime == 0):
            return False
    return True

@app.route('/primes', methods=['POST'])
def add_prime():
    if(calculated == False):
        calc_primes()
    if(len(request.args) == 0 or 'n' not in request.args):
        abort(400)

    prime_to_add = int(request.args['n'])
    if(prime_to_add in primes or check_if_prime(prime_to_add) == False):
        abort(400)
    primes.append(prime_to_add)
    return jsonify(prime_to_add), 201


@app.route('/primes', methods=['DELETE'])
def delete_prime():
    if(calculated == False):
        calc_primes()
    if(len(request.args) == 0 or 'n' not in request.args):
        abort(400)

    prime_to_delete = int(request.args['n'])
    if(prime_to_delete not in primes):
        abort(400)
    primes.remove(prime_to_delete)
    return jsonify({'result': True})


@app.route('/primes', methods=['PUT'])
def update_prime():
    if(calculated == False):
        calc_primes()
    if(len(request.args) == 0 or 'n' not in request.args or 'val' not in request.args):
        abort(400)

    index_to_update = int(request.args['n'])
    val = int(request.args['val'])
    if(index_to_update < 1 or index_to_update > len(primes) or check_if_prime(val) == False):
        abort(400)
    primes[index_to_update - 1] = val
    return jsonify(val)
