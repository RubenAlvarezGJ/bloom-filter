import matplotlib.pyplot as plt
import numpy as np
from typing import List
from .bloom_filter import BloomFilter
import random


def generate_random_set(n: int, universe_size: int) -> set[int]:
    return set(random.sample(range(1, universe_size), n))


def compute_empirical_fpr(
    bloom: BloomFilter, S: set[int], universe_size: int, query_count: int = 100000
) -> float:
    false_positives = 0
    for _ in range(query_count):
        x = random.randint(1, universe_size)
        if x not in S and bloom.contains(x):
            false_positives += 1
    return false_positives / query_count


def analysis(
    c: int,
    n: int,
    universe_size: int,
    k_min: int,
    k_max: int,
    trials: int,
    hash_type: int,
):
    m = c * n
    k_values: List[int] = list(range(k_min, k_max + 1))
    empirical_fprs: List[float] = []
    theoretical_fprs: List[float] = []

    # optimal k from theoretical formula (m/n * log(2))
    k_optimal = round((m / n) * np.log(2))
    print(f"Theoretical Optimal k: {k_optimal}")

    for k in k_values:
        print(f"Running analysis for k = {k}...")
        trial_fprs = []

        for _ in range(trials):
            bloom = BloomFilter(c, n, k, hash_type)
            S = generate_random_set(n, universe_size)

            for x in S:
                bloom.add(x)

            fpr = compute_empirical_fpr(bloom, S, universe_size)
            trial_fprs.append(fpr)

        median_fpr = np.median(trial_fprs)
        empirical_fprs.append(median_fpr)

        # theoretical FPR formula: (1 - e^(-kn/m))^k
        p = (1 - np.exp(-k * n / m)) ** k
        theoretical_fprs.append(p)

        print(f"  Median Empirical FPR: {median_fpr:.6f}, Theoretical FPR: {p:.6f}")

    # plotting
    plt.plot(k_values, empirical_fprs, "ro-", label="Empirical FPR")
    plt.plot(k_values, theoretical_fprs, "b--", label="Theoretical FPR")
    plt.axvline(x=k_optimal, color="green", linestyle="--", label=f"Optimal k = {k_optimal}")
    plt.xlabel("Number of Hash Functions (k)")
    plt.ylabel("False Positive Rate")
    plt.title(f"False Positive Rate vs. Number of Hash Functions (c = {c})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.savefig("hash_plot.png") NOTE; uncomment this line if you want a plot image