
def distribute_orders(total_orders, thread_count):
    """
    Distribute orders equally among threads using
    Static Distribution.
    """

    if total_orders < 0:
        raise ValueError("Total orders cannot be negative.")

    if thread_count <= 0:
        raise ValueError("Thread count must be positive.")

    # Calculate base orders and remaining orders
    base, remainder = divmod(total_orders, thread_count)

    # Store orders assigned to each thread
    distribution = []

    # First order ID
    start = 1

    for i in range(thread_count):

        # Give one extra order to the first threads
        count = base + (1 if i < remainder else 0)

        # Generate order IDs for this thread
        orders = list(range(start, start + count))

        distribution.append(orders)

        # Move to the next available order
        start += count

    return distribution
