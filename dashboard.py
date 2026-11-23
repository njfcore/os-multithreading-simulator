
import tkinter as tk
from tkinter import ttk, messagebox

import queue
import threading
import time

from distribution import distribute_orders
from simulation import run_simulation


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.root.title("OS Multithreading Simulator")
        self.root.geometry("1150x800")
        self.root.minsize(950, 700)
        self.root.configure(bg="#111827")

        # Colors
        self.colors = {
            "background": "#111827",
            "panel": "#1F2937",
            "panel_light": "#273449",
            "primary": "#3B82F6",
            "success": "#10B981",
            "danger": "#EF4444",
            "text": "#F9FAFB",
            "muted": "#9CA3AF",
            "border": "#374151"
        }

        # Communication queue
        self.events = queue.Queue()

        # Simulation state
        self.running = False
        self.start_time = None
        self.thread_status = {}
        self.stop_event = None
        self.current_total_orders = 0

        # Configure styles
        self.setup_styles()

        # Create interface
        self.create_header()
        self.create_statistics()
        self.create_controls()
        self.create_thread_table()
        self.create_log()

        # Start checking events
        self.root.after(100, self.process_events)

    # ----------------------------------
    # Styles
    # ----------------------------------

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["panel"],
            rowheight=32,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.colors["panel_light"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", self.colors["primary"])],
            foreground=[("selected", "white")]
        )

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=self.colors["panel_light"],
            background=self.colors["primary"],
            thickness=14,
            borderwidth=0
        )

    # ----------------------------------
    # Header
    # ----------------------------------

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        tk.Label(
            header,
            text="OS Multithreading Simulator",
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Online Store Order Processing",
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(5, 0))

    # ----------------------------------
    # Statistics
    # ----------------------------------

    def create_statistics(self):

        stats_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        stats_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        stats_frame.columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        self.total_orders_value = self.create_stat_card(
            stats_frame, 0, "Total Orders", "100"
        )

        self.threads_value = self.create_stat_card(
            stats_frame, 1, "Active Threads", "0"
        )

        self.completed_value = self.create_stat_card(
            stats_frame, 2, "Completed Orders", "0 / 100"
        )

        self.elapsed_value = self.create_stat_card(
            stats_frame, 3, "Elapsed Time", "0.00 s"
        )

        # Overall Progress
        progress_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        progress_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 15)
        )

        progress_header = tk.Frame(
            progress_frame,
            bg=self.colors["background"]
        )

        progress_header.pack(
            fill="x",
            pady=(0, 8)
        )

        tk.Label(
            progress_header,
            text="Overall Progress",
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        self.progress_percentage = tk.Label(
            progress_header,
            text="0%",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=("Segoe UI", 11, "bold")
        )

        self.progress_percentage.pack(side="right")

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0
        )

        self.progress_bar.pack(fill="x")

    def create_stat_card(self, parent, column, title, value):

        card = tk.Frame(
            parent,
            bg=self.colors["panel"],
            padx=15,
            pady=15
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5,
            pady=5
        )

        tk.Label(
            card,
            text=title,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 19, "bold")
        )

        value_label.pack(anchor="w", pady=(8, 0))

        return value_label

    # ----------------------------------
    # Controls
    # ----------------------------------

    def create_controls(self):

        controls = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=15,
            pady=15
        )

        controls.pack(
            fill="x",
            padx=25,
            pady=10
        )

        tk.Label(
            controls,
            text="Orders:",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 8))

        self.orders_input = tk.Spinbox(
            controls,
            from_=1,
            to=10000,
            width=8,
            font=("Segoe UI", 11)
        )

        self.orders_input.delete(0, "end")
        self.orders_input.insert(0, "100")

        self.orders_input.pack(side="left", padx=(0, 20))

        tk.Label(
            controls,
            text="Threads:",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 8))

        self.threads_input = tk.Spinbox(
            controls,
            from_=1,
            to=150,
            width=8,
            font=("Segoe UI", 11)
        )

        self.threads_input.delete(0, "end")
        self.threads_input.insert(0, "10")

        self.threads_input.pack(side="left", padx=(0, 20))

        self.start_button = tk.Button(
            controls,
            text="Start Simulation",
            bg=self.colors["success"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.start_simulation
        )

        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(
            controls,
            text="Stop Simulation",
            bg=self.colors["danger"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            state="disabled",
            command=self.stop_simulation
        )

        self.stop_button.pack(side="left", padx=5)

    # ----------------------------------
    # Thread Table
    # ----------------------------------

    def create_thread_table(self):

        container = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        tk.Label(
            container,
            text="Thread Monitoring",
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(
            container,
            bg=self.colors["panel"]
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "thread_id",
            "orders",
            "completed",
            "progress",
            "status",
            "execution_time"
        )

        self.thread_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.thread_table.heading(
            "thread_id",
            text="Thread ID"
        )

        self.thread_table.heading(
            "orders",
            text="Orders"
        )

        self.thread_table.heading(
            "completed",
            text="Completed"
        )

        self.thread_table.heading(
            "progress",
            text="Progress"
        )

        self.thread_table.heading(
            "status",
            text="Status"
        )

        self.thread_table.heading(
            "execution_time",
            text="Execution Time"
        )

        self.thread_table.column(
            "thread_id",
            width=90,
            anchor="center"
        )

        self.thread_table.column(
            "orders",
            width=100,
            anchor="center"
        )

        self.thread_table.column(
            "completed",
            width=110,
            anchor="center"
        )

        self.thread_table.column(
            "progress",
            width=100,
            anchor="center"
        )

        self.thread_table.column(
            "status",
            width=130,
            anchor="center"
        )

        self.thread_table.column(
            "execution_time",
            width=140,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.thread_table.yview
        )

        self.thread_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.thread_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ----------------------------------
    # Log
    # ----------------------------------

    def create_log(self):

        log_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        log_frame.pack(
            fill="x",
            padx=25,
            pady=(10, 20)
        )

        tk.Label(
            log_frame,
            text="Simulation Log",
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.log_text = tk.Text(
            log_frame,
            height=6,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Consolas", 9),
            relief="flat",
            state="disabled"
        )

        self.log_text.pack(fill="x")

    def add_log(self, message):

        self.log_text.config(state="normal")

        timestamp = time.strftime("%H:%M:%S")

        self.log_text.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.log_text.see("end")

        self.log_text.config(state="disabled")

    # ----------------------------------
    # Start Simulation
    # ----------------------------------

    def start_simulation(self):

        if self.running:
            return

        try:

            total_orders = int(self.orders_input.get())
            thread_count = int(self.threads_input.get())

            if not 1 <= total_orders <= 10000:
                raise ValueError(
                    "Orders must be between 1 and 10000."
                )

            if not 1 <= thread_count <= 150:
                raise ValueError(
                    "Threads must be between 1 and 150."
                )

        except ValueError as error:

            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

            return

        # Distribute orders
        distribution = distribute_orders(
            total_orders,
            thread_count
        )

        # Reset dashboard
        for item in self.thread_table.get_children():
            self.thread_table.delete(item)

        self.thread_status = {}

        self.current_total_orders = total_orders

        self.total_orders_value.config(
            text=str(total_orders)
        )

        self.threads_value.config(text="0")

        self.completed_value.config(
            text=f"0 / {total_orders}"
        )

        self.elapsed_value.config(text="0.00 s")

        self.progress_bar["value"] = 0

        self.progress_percentage.config(text="0%")

        # Clear old events
        while not self.events.empty():
            try:
                self.events.get_nowait()
            except queue.Empty:
                break

        # Prepare thread table
        for thread_id, orders in enumerate(
            distribution,
            start=1
        ):

            self.thread_table.insert(
                "",
                "end",
                iid=str(thread_id),
                values=(
                    thread_id,
                    len(orders),
                    0,
                    "0%",
                    "Waiting",
                    "-"
                )
            )

            self.thread_status[thread_id] = "Waiting"

        # Start simulation
        self.running = True

        self.start_time = time.perf_counter()

        self.stop_event = threading.Event()

        self.start_button.config(state="disabled")

        self.stop_button.config(state="normal")

        self.add_log(
            f"Simulation started: {total_orders} orders, "
            f"{thread_count} threads."
        )

        # Run simulation in background
        simulation_thread = threading.Thread(
            target=self.run_simulation_background,
            args=(total_orders, thread_count),
            daemon=True
        )

        simulation_thread.start()

    # ----------------------------------
    # Background Simulation
    # ----------------------------------

    def run_simulation_background(
        self,
        total_orders,
        thread_count
    ):

        try:

            total_time, thread_times = run_simulation(
                total_orders=total_orders,
                thread_count=thread_count,
                verbose=False,
                show_summary=False,
                progress_callback=self.events.put,
                stop_event=self.stop_event
            )

            self.events.put({
                "event": "simulation_finished",
                "total_time": total_time
            })

        except Exception as error:

            self.events.put({
                "event": "simulation_error",
                "message": str(error)
            })

    # ----------------------------------
    # Stop Simulation
    # ----------------------------------

    def stop_simulation(self):

        if not self.running:
            return

        self.stop_event.set()

        self.stop_button.config(state="disabled")

        self.add_log(
            "Stop requested. Waiting for active orders to finish..."
        )

    # ----------------------------------
    # Process Events
    # ----------------------------------

    def process_events(self):

        while True:

            try:
                event = self.events.get_nowait()

            except queue.Empty:
                break

            event_type = event["event"]

            thread_id = event.get("thread_id")

            # Thread started
            if event_type == "thread_started":

                self.thread_status[thread_id] = "Processing"

                self.thread_table.set(
                    str(thread_id),
                    "status",
                    "Processing"
                )

                active_count = sum(
                    status == "Processing"
                    for status in self.thread_status.values()
                )

                self.threads_value.config(
                    text=str(active_count)
                )

                self.add_log(
                    f"Thread {thread_id} started."
                )

            # Order completed
            elif event_type == "order_completed":

                item_id = str(thread_id)

                current_values = self.thread_table.item(
                    item_id,
                    "values"
                )

                completed = int(current_values[2]) + 1

                total_thread_orders = int(current_values[1])

                thread_percentage = (
                    completed / total_thread_orders
                ) * 100 if total_thread_orders > 0 else 0

                # Update completed orders
                self.thread_table.set(
                    item_id,
                    "completed",
                    completed
                )

                # Update thread progress
                self.thread_table.set(
                    item_id,
                    "progress",
                    f"{thread_percentage:.0f}%"
                )

                # Calculate total completed orders
                total_completed = sum(
                    int(
                        self.thread_table.set(
                            item,
                            "completed"
                        )
                    )
                    for item in self.thread_table.get_children()
                )

                total_orders = self.current_total_orders

                # Update completed orders card
                self.completed_value.config(
                    text=f"{total_completed} / {total_orders}"
                )

                # Calculate overall progress
                percentage = (
                    total_completed / total_orders
                ) * 100 if total_orders > 0 else 0

                # Update overall progress bar
                self.progress_bar["value"] = percentage

                self.progress_percentage.config(
                    text=f"{percentage:.0f}%"
                )

            # Thread completed
            elif event_type == "thread_finished":

                self.thread_status[thread_id] = "Completed"

                self.thread_table.set(
                    str(thread_id),
                    "status",
                    "Completed"
                )

                self.thread_table.set(
                    str(thread_id),
                    "execution_time",
                    f"{event['elapsed_time']:.2f} s"
                )

                active_count = sum(
                    status == "Processing"
                    for status in self.thread_status.values()
                )

                self.threads_value.config(
                    text=str(active_count)
                )

                self.add_log(
                    f"Thread {thread_id} completed."
                )

            # Thread stopped
            elif event_type == "thread_stopped":

                self.thread_status[thread_id] = "Stopped"

                self.thread_table.set(
                    str(thread_id),
                    "status",
                    "Stopped"
                )

                self.thread_table.set(
                    str(thread_id),
                    "execution_time",
                    f"{event['elapsed_time']:.2f} s"
                )

                active_count = sum(
                    status == "Processing"
                    for status in self.thread_status.values()
                )

                self.threads_value.config(
                    text=str(active_count)
                )

                self.add_log(
                    f"Thread {thread_id} stopped."
                )

            # Simulation finished
            elif event_type == "simulation_finished":

                self.running = False

                self.elapsed_value.config(
                    text=f"{event['total_time']:.2f} s"
                )

                self.start_button.config(state="normal")

                self.stop_button.config(state="disabled")

                if self.stop_event and self.stop_event.is_set():

                    self.add_log(
                        f"Simulation stopped after "
                        f"{event['total_time']:.2f} seconds."
                    )

                else:

                    self.add_log(
                        f"Simulation completed in "
                        f"{event['total_time']:.2f} seconds."
                    )

            # Simulation error
            elif event_type == "simulation_error":

                self.running = False

                self.start_button.config(state="normal")

                self.stop_button.config(state="disabled")

                messagebox.showerror(
                    "Simulation Error",
                    event["message"]
                )

                self.add_log(
                    f"Error: {event['message']}"
                )

        # Update elapsed time
        if self.running and self.start_time is not None:

            elapsed = time.perf_counter() - self.start_time

            self.elapsed_value.config(
                text=f"{elapsed:.2f} s"
            )

        # Check for new events
        self.root.after(
            100,
            self.process_events
        )


# ----------------------------------
# Main
# ----------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = Dashboard(root)

    root.mainloop()
