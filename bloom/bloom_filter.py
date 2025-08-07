from typing import List
from bitarray import bitarray
import random

MERSENNE_POWER = 61
MERSENNE_PRIME = 2 ** MERSENNE_POWER - 1
UNIVERSE_SIZE = 2 ** 60

class BloomFilter:
    def __init__(self, c: int, n: int, k: int, hash_type: int = 1) -> None:
        if hash_type not in (1, 2):
            raise ValueError("hash_type must be 1 or 2")

        self.c = c
        self.n = n
        self.k = k
        self.hash_type = hash_type

        self.m = c * n
        self.N = UNIVERSE_SIZE
        self.p = MERSENNE_PRIME

        self.table = bitarray(self.m)
        self.table.setall(0)
        self.seeds: List[int] = []
        self.create_seeds()

    def create_seeds(self) -> None:
        for _ in range(self.k):
            self.seeds.append(random.getrandbits(32))

    def get_random(self, lower_bound: int, upper_bound: int, seed: int) -> int:
        rng = random.Random(seed)
        return rng.randint(lower_bound, upper_bound)

    def h1(self, value: int, seed: int) -> int:
        rng = random.Random(seed)
        a = rng.randint(1, self.p - 1)
        b = rng.randint(0, self.p - 1)
        return ((a * value + b) % self.p) % self.m

    def h2(self, value: int, seed: int) -> int:
        s = value + seed
        rng = random.Random(s)
        return rng.randint(0, self.m - 1)

    def add(self, x: int) -> None:
        for i in range(self.k):
            seed = self.seeds[i]
            if self.hash_type == 1:
                index = self.h1(x, seed)
            else:
                index = self.h2(x, seed)
            self.table[index] = 1

    def contains(self, x: int) -> bool:
        for i in range(self.k):
            seed = self.seeds[i]
            if self.hash_type == 1:
                index = self.h1(x, seed)
            else:
                index = self.h2(x, seed)
            if not self.table[index]:
                return False
        return True