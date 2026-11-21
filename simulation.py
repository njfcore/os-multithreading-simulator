
import time
import threading

from distribution import distribute_orders
from worker import process_orders


def run_worker(thread_id, orders, results):
    """
    Run a worker and save its execution time.
    """

    elapsed_time = process_orders(thread_id, orders)

    results[thread_id - 1] = elapsed_time


def run_simulation(total_orders, thread_count):

    # Distribute orders among threads
    distribution = distribute_orders(total_orders, thread_count)

    # Store thread execution times
    results = [0] * thread_count

    # Store all thread objects
    threads = []

    # Start measuring total execution time
    start_time = time.perf_counter()

    # Create threads
    for i in range(thread_count):

        thread = threading.Thread(
            target=run_worker,
            args=(i + 1, distribution[i], results)
        )

        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Calculate total execution time
    end_time = time.perf_counter()
    total_time = end_time - start_time

    print("\n========== Simulation Results ==========")
    print(f"Total orders: {total_orders}")
    print(f"Number of threads: {thread_count}")
    print(f"Total execution time: {total_time:.2f} seconds")

    print("\n---------- Thread Results ----------")

    for i, elapsed in enumerate(results):
        print(f"Thread {i + 1}: {elapsed:.2f} seconds")

    return total_time, results


if __name__ == "__main__":
    run_simulation(total_orders=6, thread_count=3)
