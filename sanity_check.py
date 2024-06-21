import time

from paragraphs import generate_random_paragraph


def time_function(f):
    start = time.time()
    _ = f()
    end = time.time()
    total_time = end - start
    return total_time


test_times = [time_function(generate_random_paragraph) for _ in range(0, 1000)]
mean_time = sum(test_times) / len(test_times)

print(f"Average time: {mean_time:.5f}")
