# Implementation of RSA and One-Way Permutations
**Cryptography CS5830 - Jake Magid - jm2644@cornell.edu**

## Usage
The file can be called from the terminal as `python oneway.py` and will generate x, f(x), and x_ret using RSA implementation and trapdoor. This will also print a safe prime number with `n_in` bits. Change this value as necessary.

Other functions can be tested in the `Print Section` of the code by uncommenting them and manipulating the inputs as necessary.

## Functions and Classes
* **Extended Euclid** </br>
`extendedeuclid(a,b)`</br>
Input: Two values `a` and `b` </br>
Output: `x,y` such that `ax + by = 1`

* **Inverse Modulus** </br>
`inv_mod(a,b)` </br>
Input: Two values `a` and `b` </br>
Output: Modular inverse of `a mod b` (i.e. `x` such that `ax mod b = 1`)

* **Exponential Modulus** </br>
`exp_mod(a,x,N)` </br>
Input: Values `a, x, N` </br>
Output: `a^x mod N`

* **Miller-Rabin Primality Test** </br>
`is_prime(n)` </br>
Input: odd integer `n` to be tested for primality </br>
Output: `True` if number is probably prime, `False` if number is composite

* **Random n-bit Prime** </br>
`rand_nbit_prime(n)` </br>
Input: max number of bits `n` which prime number can be represented by </br>
Output: random prime integer that can be represented using `n` bits

* **Random n-bit Safe Prime** </br>
`rand_nbit_safe_prime(n)` </br>
Input: number of bits to find a safe prime `n` </br>
Output: `p`, an n-bit safe prime and `q`, the corresponding Sophie Germain prime

* **Random n-bit Safe Prime Generator** </br>
`rand_nbit_safe_prime_generator(n)` </br>
Input: number of bits to find a safe prime `n` </br>
Output: `p`, an n-bit safe prime and `g`, a generator for Z<sub>p</sub>*

* **Exponentiation One Way Permutation** </br>
`class exponentiation_OWP`
  * `gen(n)` </br>
  Input: number of bits `n` </br>
  Output: `p`, an n-bit safe prime and `g`, a generator for Z<sub>p</sub>*
  
  * `sample(p)` </br>
  Input: `p` from `gen()` </br>
  Output: `x`, a random integer from `1` to `p-1`
  
  * `evaluate(p,g,x)` </br>
  Input: `p,g,x` from `gen()` and `sample()` </br>
  Output: `fx` which is `g^x mod p`
  
* **RSA One Way Permutation** </br>
`class RSA_OWP`
  * `gen(n)` </br>
  Input: number of bits `n` for `p` and `q` </br>
  Output: The public keys `N,e` and the private trapdoor key `d`. </br>
  `N` is `p*q`. `e` is a random integer from 2 to `phi-1` where `phi = (p-1)*(q-1)`. `d` is the inverse modulus of `e` and `phi`.
  
  * `sample(N)` </br>
  Input: `N` from `gen()` </br>
  Output: `x`, a random integer from `1` to `N`
  
  * `evaluate(x,e,N)` </br>
  Input: `x,e,N` from `gen()` and `sample()` </br>
  Output: `fx` which is `x^e mod N`
  
* **Trapdoor for RSA** </br>
`trapdoor(fx, d, N)` </br>
Input: `fx, d, N` from `RSA_OWP.gen()`, `RSA_OWP.sample()`, and `RSA_OWP.evaluate()` </br>
Output: The corresponding `x` that produced `fx`. The magic here is that `x` can be retrieved from `fx` using the public information `N`, and the private key `d`.
  
