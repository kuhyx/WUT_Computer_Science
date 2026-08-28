"""Sieve of Eratosthenes: every prime up to and including N."""

import math
import sys


def sieve_of_eratosthenes(num: int) -> list[int]:
    """Return every prime from 1 to num.

    Args:
        num (int): Number up to which the prime numbers should be printed

    Returns:
        list[int]: List of prime numbers

    """
    if num <= 0:
        msg = "Number should not be negative."
        raise ValueError(msg)
    # boolean list to store if a number is prime or not
    prime = [True] * (num + 1)
    p = 2  # starting prime number
    # Stop at sqrt(num): a composite always has a factor at or below its
    # square root, so anything still marked prime past that point stays prime.
    while p <= math.sqrt(num):
        # If prime[p] is not
        # changed, then it is a prime
        if prime[p]:
            i = p << 1  # i = p * 2
            # Updating all multiples of p
            while i <= num:
                prime[i] = False
                i += p
        p += 1
    return [p for p in range(2, num + 1) if prime[p]]


def print_sieve(num: int) -> None:
    """Print every prime from 1 to num, space separated.

    Args:
        num (int): Number up to which the prime numbers should be printed

    """
    sys.stdout.write(" ".join(str(n) for n in sieve_of_eratosthenes(num)))
    sys.stdout.write("\n")


# Driver code
if __name__ == "__main__":
    bound = int(input("Enter a number: "))
    sys.stdout.write(
        f"Following are the prime numbers smaller than or equal to {bound}\n"
    )
    print_sieve(bound)
