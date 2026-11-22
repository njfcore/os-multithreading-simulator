
import time


def process_orders(thread_id, orders, verbose=True):
    """
    Process all orders assigned to a thread.
    """

    start_time = time.perf_counter()

    if verbose:
        print(f"[Thread {thread_id}] Started processing {len(orders)} orders.")

    for order_id in orders:

        if verbose:
            print(f"[Thread {thread_id}] Processing order #{order_id}")

        # Simulate order processing
        time.sleep(1)

        if verbose:
            print(f"[Thread {thread_id}] Order #{order_id} completed.")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if verbose:
        print(
            f"[Thread {thread_id}] Finished! "
            f"Execution time: {elapsed_time:.2f} seconds."
        )

    return elapsed_time