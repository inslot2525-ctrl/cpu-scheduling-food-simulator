"""
CPU Scheduling Food Simulator
Main entry point for the simulation.

This simulator demonstrates CPU scheduling algorithms using food orders as an analogy:
- Orders = Processes
- Preparation Time = Burst Time
- Kitchen = CPU
- Priority = Process Priority
"""
from scheduler_engine import Order, run_fcfs, run_sjf, run_priority, run_round_robin
from metrics import PerformanceMetrics, compare_algorithms
from visualization import show_dashboard, Dashboard


def create_sample_orders():
    """Create a sample set of food orders for demonstration."""
    return [
        Order(1, "Pizza", arrival_time=0, preparation_time=8, priority=2),
        Order(2, "Burger", arrival_time=1, preparation_time=4, priority=1),
        Order(3, "Salad", arrival_time=2, preparation_time=2, priority=3),
        Order(4, "Pasta", arrival_time=3, preparation_time=6, priority=2),
        Order(5, "Soup", arrival_time=4, preparation_time=3, priority=4),
    ]


def run_simulation():
    """Run the complete simulation with all algorithms."""
    print("\n" + "=" * 70)
    print(" " * 15 + "CPU SCHEDULING FOOD SIMULATOR")
    print(" " * 10 + "Demonstrating OS Scheduling Algorithms")
    print("=" * 70)
    
    # Create sample orders
    orders = create_sample_orders()
    
    print("\n📋 INITIAL ORDERS:")
    print("-" * 50)
    for order in orders:
        print(f"  {order.name:<10} | Arrival: {order.arrival_time} | "
              f"Prep Time: {order.preparation_time} | Priority: {order.priority}")
    print("-" * 50)
    
    # Dictionary to store results for comparison
    all_results = {}
    
    # 1. First Come First Served
    print("\n" + "=" * 70)
    print("ALGORITHM 1: FIRST COME FIRST SERVED (FCFS)")
    print("=" * 70)
    fcfs_orders, fcfs_gantt = run_fcfs(create_sample_orders())
    print(show_dashboard(fcfs_orders, fcfs_gantt, "FCFS"))
    all_results["FCFS"] = (fcfs_orders, fcfs_gantt)
    
    # 2. Shortest Job First (Non-preemptive)
    print("\n" + "=" * 70)
    print("ALGORITHM 2: SHORTEST JOB FIRST (SJF)")
    print("=" * 70)
    sjf_orders, sjf_gantt = run_sjf(create_sample_orders(), preemptive=False)
    print(show_dashboard(sjf_orders, sjf_gantt, "SJF"))
    all_results["SJF"] = (sjf_orders, sjf_gantt)
    
    # 3. Shortest Remaining Time First (Preemptive SJF)
    print("\n" + "=" * 70)
    print("ALGORITHM 3: SHORTEST REMAINING TIME FIRST (SRTF)")
    print("=" * 70)
    srtf_orders, srtf_gantt = run_sjf(create_sample_orders(), preemptive=True)
    print(show_dashboard(srtf_orders, srtf_gantt, "SRTF"))
    all_results["SRTF"] = (srtf_orders, srtf_gantt)
    
    # 4. Priority Scheduling (Non-preemptive)
    print("\n" + "=" * 70)
    print("ALGORITHM 4: PRIORITY SCHEDULING")
    print("=" * 70)
    priority_orders, priority_gantt = run_priority(create_sample_orders(), preemptive=False)
    print(show_dashboard(priority_orders, priority_gantt, "Priority"))
    all_results["Priority"] = (priority_orders, priority_gantt)
    
    # 5. Round Robin
    print("\n" + "=" * 70)
    print("ALGORITHM 5: ROUND ROBIN (Quantum = 3)")
    print("=" * 70)
    rr_orders, rr_gantt = run_round_robin(create_sample_orders(), time_quantum=3)
    print(show_dashboard(rr_orders, rr_gantt, "Round Robin"))
    all_results["Round Robin"] = (rr_orders, rr_gantt)
    
    # Comparison Dashboard
    dashboard = Dashboard("Algorithm Comparison")
    print(dashboard.compare_algorithms(all_results))
    
    return all_results


def interactive_mode():
    """Run the simulator in interactive mode."""
    print("\n" + "=" * 70)
    print(" " * 10 + "INTERACTIVE CPU SCHEDULING FOOD SIMULATOR")
    print("=" * 70)
    
    orders = []
    
    print("\nEnter your food orders (type 'done' when finished):")
    order_id = 1
    
    while True:
        print(f"\n--- Order {order_id} ---")
        name = input("Food name (or 'done' to finish): ").strip()
        
        if name.lower() == 'done':
            break
        
        try:
            arrival = int(input("Arrival time: "))
            prep_time = int(input("Preparation time: "))
            priority = int(input("Priority (1=highest): "))
            
            orders.append(Order(order_id, name, arrival, prep_time, priority))
            order_id += 1
            print(f"✓ Added: {name}")
        except ValueError:
            print("Invalid input. Please enter numbers for time values.")
            continue
    
    if not orders:
        print("No orders entered. Using sample orders.")
        orders = create_sample_orders()
    
    print("\nSelect scheduling algorithm:")
    print("1. First Come First Served (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Shortest Remaining Time First (SRTF)")
    print("4. Priority Scheduling")
    print("5. Round Robin")
    print("6. Compare All")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '1':
        result_orders, gantt = run_fcfs(orders)
        print(show_dashboard(result_orders, gantt, "FCFS"))
    elif choice == '2':
        result_orders, gantt = run_sjf(orders, preemptive=False)
        print(show_dashboard(result_orders, gantt, "SJF"))
    elif choice == '3':
        result_orders, gantt = run_sjf(orders, preemptive=True)
        print(show_dashboard(result_orders, gantt, "SRTF"))
    elif choice == '4':
        result_orders, gantt = run_priority(orders, preemptive=False)
        print(show_dashboard(result_orders, gantt, "Priority"))
    elif choice == '5':
        quantum = int(input("Enter time quantum: "))
        result_orders, gantt = run_round_robin(orders, time_quantum=quantum)
        print(show_dashboard(result_orders, gantt, f"Round Robin (q={quantum})"))
    elif choice == '6':
        # Run all algorithms and compare
        from copy import deepcopy
        results = {
            "FCFS": run_fcfs(deepcopy(orders)),
            "SJF": run_sjf(deepcopy(orders), preemptive=False),
            "SRTF": run_sjf(deepcopy(orders), preemptive=True),
            "Priority": run_priority(deepcopy(orders), preemptive=False),
            "Round Robin": run_round_robin(deepcopy(orders), time_quantum=3)
        }
        dashboard = Dashboard("Algorithm Comparison")
        print(dashboard.compare_algorithms(results))
    else:
        print("Invalid choice")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        run_simulation()
