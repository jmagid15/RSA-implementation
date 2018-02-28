import random
import sys
sys.setrecursionlimit(1000000)

def extendedeuclid(a,b):
    if a % b == 0:
        return (0,1)
    else:
        (x, y) = extendedeuclid(b, a % b)
        return (y, x - y * (a//b))

def inv_mod(a,b):
    # Returns modular inverse of a mod b
    x, y = extendedeuclid(a, b)
    return x % b

def exp_mod(a,x,N):
    # Returns a^x mod N
    r = 1
    while x > 0:
        if x % 2 != 0:
            r = r*a % N
        x = x//2
        a = a**2 % N
    return r

def is_prime(n):
    # Using Miller-Rabin algorithm
    # Input n: odd integer to be tested for primality
    # Input k: parameter to determine accuracy of test
    # Output: either False for 'composite' or True for 'probably prime'

    if n == 2:
        return True
    if n <= 1:
        return False
    if n > 2 and n % 2 ==0:
        return False

    # Factor n-1 as 2^j * u where t is odd
    j = 0
    u = n - 1
    while u % 2 == 0:
        j = j + 1
        u = u//2

    # u and j are now tuned so that n - 1 = u * 2^j

    # Choose random alpha 10 times. If any of them fail -> composite.
    for i in range(10):
        a = random.randint(1, n - 1)

        if exp_mod(a, n-1, n) != 1:
            return False

        if exp_mod(a, u*(2**(j+1)), n) == 1 and exp_mod(a, u*(2**(j)), n) != 1:
            return False

    return True


def rand_nbit_prime(n):
    # Input n: number of bits to find a prime
    # Output: random prime integer that can be represented with n bits
    if n<1:
        return NotImplementedError

    x = random.getrandbits(n)
    while not is_prime(x):
        x = random.getrandbits(n)

    return x


def rand_nbit_safe_prime(n):
    # Input n: number of bits to find a safe prime
    # Output p: n-bit safe prime
    # Output q: corresponding prime

    # Choose an nbit prime
    p = rand_nbit_prime(n)

    #See if there is another prime q s.t. p = 2q + 1
    q = (p-1)//2

    # Rinse and repeat until we find a p and q that are both prime
    while not is_prime(q):
        # Choose an nbit prime
        p = rand_nbit_prime(n)

        #See if there is another prime q s.t. p = 2q + 1
        q = (p-1)//2

    return p, q

def rand_nbit_safe_prime_generator(n):
    # Input n: number of bits to find a safe prime
    # Output p: n-bit safe prime
    # Output g: generator for Zp*


    # Choose an n-bit safe prime
    p, q = rand_nbit_safe_prime(n)

    g = random.randint(1, p-1)

    while not (abs(g % p) != 1 and abs(exp_mod(g,q,p)) != 1):
        # Choose an n-bit safe prime
        p, q = rand_nbit_safe_prime(n)

        g = random.randint(1, p-1)

    return p, g


class exponentiation_OWP:

    def gen(n):
        # Input n: number of bits
        # Output p, g
        p, g = rand_nbit_safe_prime_generator(n)
        return p, g

    def sample(p):
        # Input p from gen()
        # Output x
        x = random.randint(1, p-1)
        return x

    def evaluate(p, g, x):
        # Input p,g,x
        # Output fx
        return exp_mod(g, x, p)


class RSA_OWP:

    def gen(self, n):
        # Input n: number of bits for p and q
        # Output N,e,d
        p = rand_nbit_prime(n)
        q = rand_nbit_prime(n)
        phi = (p-1)*(q-1)
        N = p * q
        e = random.randint(2,phi - 1)
        x, y = extendedeuclid(e, phi)
        while x*e + y*phi != 1:
            e = random.randint(2,phi - 1)
            x, y = extendedeuclid(e, phi)
        d = inv_mod(e, phi)
        return N, e, d

    def sample(self, N):
        x = random.randint(1, N)
        return x

    def evaluate(self, x, e, N):
        fx = exp_mod(x, e, N)
        return fx


def trapdoor(fx, d, N):
    # Inputs : fx, d, N
    # Outputs : x

    x = exp_mod(fx, d, N)
    return x

#### Print Section ####
# print(extendedeuclid(4, 15))
# inv_mod(3,7)
# exp_mod(3,3,5)
# is_prime(309851)
# rand_nbit_prime(20)
# rand_nbit_safe_prime(10)
# rand_nbit_safe_prime_generator(8)


#### RSA and trapdoor ####
print('-'*50)
print('Generating x, f(x), x_ret using RSA implementation and trapdoor...')

# Set n bits (aka how long of a safe prime do you want)
cls_inst = RSA_OWP()
N, e, d = cls_inst.gen(2048)
x = cls_inst.sample(N)
fx = cls_inst.evaluate(x, e, N)
print('x: ', x, '\n')
print('fx: ', fx, '\n')

x_ret = trapdoor(fx, d, N)
print('x_ret: ', x_ret, '\n')
print('Does x = x_ret? ' x == x_ret)


#### Safe prime as big as possible ####
print('-'*50)
n_in = 512
print('Finding a safe prime of at least', n_in, 'bits...')
p, q = rand_nbit_safe_prime(n_in)
print('p: ', p, '\n')
print('q: ', q)
