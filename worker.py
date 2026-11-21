
import time


def process_orders(thread_id, orders):
    """
    Process all orders assigned to a thread.
    """

    # Record the starting time
    start_time = time.perf_counter()

    print(f"[Thread {thread_id}] Started processing {len(orders)} orders.")

    # Process orders one by one
    for order_id in orders:

        print(f"[Thread {thread_id}] Processing order #{order_id}")

        # Simulate order processing
        time.sleep(1)

        print(f"[Thread {thread_id}] Order #{order_id} completed.")

    # Calculate total execution time
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(
        f"[Thread {thread_id}] Finished! "
        f"Execution time: {elapsed_time:.2f} seconds."
    )

    return elapsed_time
