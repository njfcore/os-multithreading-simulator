
import time


def process_orders(
    thread_id,
    orders,
    verbose=True,
    progress_callback=None,
    stop_event=None
):
    """
    Process all orders assigned to a thread.
    """

    start_time = time.perf_counter()

    if verbose:
        print(
            f"[Thread {thread_id}] "
            f"Started processing {len(orders)} orders."
        )

    if progress_callback:
        progress_callback({
            "event": "thread_started",
            "thread_id": thread_id,
            "total_orders": len(orders)
        })

    for order_id in orders:

        # Check whether the simulation should stop
        if stop_event and stop_event.is_set():
            break

        if verbose:
            print(
                f"[Thread {thread_id}] "
                f"Processing order #{order_id}"
            )

        time.sleep(1)

        if verbose:
            print(
                f"[Thread {thread_id}] "
                f"Order #{order_id} completed."
            )

        if progress_callback:
            progress_callback({
                "event": "order_completed",
                "thread_id": thread_id,
                "order_id": order_id
            })

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # Determine final thread status
    stopped = stop_event and stop_event.is_set()

    if stopped:
        status = "Stopped"
    else:
        status = "Completed"

    if verbose:
        print(
            f"[Thread {thread_id}] "
            f"{status}! Execution time: {elapsed_time:.2f} seconds."
        )

    if progress_callback:
        progress_callback({
            "event": "thread_stopped" if stopped else "thread_finished",
            "thread_id": thread_id,
            "elapsed_time": elapsed_time
        })

    return elapsed_time
