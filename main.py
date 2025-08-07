from bloom.analysis import analysis

def main():
    analysis(c=10, n=1000, universe_size=10000, k_min=1, k_max=10, trials=5, hash_type=1)

if __name__ == "__main__":
    main()