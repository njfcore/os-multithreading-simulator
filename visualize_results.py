
import csv
import matplotlib.pyplot as plt


def load_results(filename="experiments_results.csv"):

    thread_counts = []
    execution_times = []
    speedups = []
    efficiencies = []

    with open(filename, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            thread_counts.append(int(row["thread_count"]))
            execution_times.append(float(row["total_time"]))
            speedups.append(float(row["speedup"]))
            efficiencies.append(float(row["efficiency"]))

    return thread_counts, execution_times, speedups, efficiencies


def plot_execution_time(thread_counts, execution_times):

    plt.figure(figsize=(10, 6))

    plt.plot(thread_counts, execution_times, marker="o")

    plt.title("Number of Threads vs Execution Time")
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig("execution_time.png")
    plt.close()


def plot_speedup(thread_counts, speedups):

    plt.figure(figsize=(10, 6))

    plt.plot(thread_counts, speedups, marker="o")

    plt.title("Number of Threads vs Speedup")
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig("speedup.png")
    plt.close()


def plot_efficiency(thread_counts, efficiencies):

    plt.figure(figsize=(10, 6))

    plt.plot(thread_counts, efficiencies, marker="o")

    plt.title("Number of Threads vs Efficiency")
    plt.xlabel("Number of Threads")
    plt.ylabel("Efficiency (%)")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig("efficiency.png")
    plt.close()


def main():

    data = load_results()

    thread_counts, execution_times, speedups, efficiencies = data

    plot_execution_time(thread_counts, execution_times)
    plot_speedup(thread_counts, speedups)
    plot_efficiency(thread_counts, efficiencies)

    print("All charts generated successfully!")


if __name__ == "__main__":
    main()
