from config import WIDTH, HEIGHT

def find_common_divisors(a, b):
    def get_divisors(n):
        divisors = set()
        for i in range(1, int(n ** 0.5) + 1):
            if n % i == 0:
                divisors.add(i)
                divisors.add(n // i)
        return divisors
    
    divisors_a = get_divisors(a)
    divisors_b = get_divisors(b)
    common_divisors = divisors_a.intersection(divisors_b)
    return sorted(common_divisors, reverse=True)

def get_availavle_cell_sizes():
    common_divisors = find_common_divisors(WIDTH, HEIGHT)

    min_reasonable_size = 5
    max_reasonable_size = min(WIDTH, HEIGHT)
    AVAILABLE_CELL_SIZES = [
        size for size in common_divisors 
        if min_reasonable_size <= size <= max_reasonable_size
    ]
    return AVAILABLE_CELL_SIZES