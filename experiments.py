
import csv

from simulation import run_simulation


TOTAL_ORDERS = 100

THREAD_COUNTS = [
    1, 3, 5, 8, 10, 20,
    25, 50, 75, 100, 120, 150
]


def run_experiments():

    results = []

    print("========== Starting Experiments ==========")

    for thread_count in THREAD_COUNTS:

        print(f"\nRunning experiment with {thread_count} threads...")

        total_time, thread_times = run_simulation(
            total_orders=TOTAL_ORDERS,
            thread_count=thread_count,
            verbose=False,
            show_summary=False
        )

        max_thread_time = max(thread_times, default=0)

        results.append({
            "thread_count": thread_count,
            "total_time": total_time,
            "max_thread_time": max_thread_time
        })

        print(
            f"Finished K={thread_count} | "
            f"Total time: {total_time:.2f} seconds"
        )

    # Calculate speedup and efficiency
    baseline_time = results[0]["total_time"]

    for result in results:

        speedup = baseline_time / result["total_time"]

        efficiency = speedup / result["thread_count"] * 100

        result["speedup"] = speedup
        result["efficiency"] = efficiency

    # Save results to CSV
    save_results(results)

    # Display final comparison table
    display_results(results)


def save_results(results):

    filename = "experiments_results.csv"

    fieldnames = [
        "thread_count",
        "total_time",
        "max_thread_time",
        "speedup",
        "efficiency"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {filename}")


def display_results(results):

    print("\n========== Final Experiment Results ==========")

    print(
        f"{'Threads':<10}"
        f"{'Total Time':<15}"
        f"{'Max Thread':<15}"
        f"{'Speedup':<12}"
        f"{'Efficiency':<12}"
    )

    print("-" * 64)

    for result in results:

        print(
            f"{result['thread_count']:<10}"
            f"{result['total_time']:<15.2f}"
            f"{result['max_thread_time']:<15.2f}"
            f"{result['speedup']:<12.2f}"
            f"{result['efficiency']:<12.2f}%"
        )


if __name__ == "__main__":
    run_experiments()
