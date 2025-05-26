import random
def generate_number_excluding(start, end, excluded_numbers, max_attempts=10):

    excluded = set(excluded_numbers)
    for _ in range(max_attempts):
        num = random.randint(start, end)
        if num not in excluded:
            return num