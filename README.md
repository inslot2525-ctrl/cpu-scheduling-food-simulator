# CPU Scheduling Food Simulator

A Python-based educational simulator that demonstrates CPU scheduling algorithms using food orders as an intuitive analogy. No external dependencies — pure Python.

## Concept

This simulator maps OS CPU scheduling concepts to a restaurant kitchen:

| CPU Scheduling Term | Food Simulator Equivalent        |
|---------------------|----------------------------------|
| Process             | Food Order                       |
| Burst Time          | Preparation Time                 |
| CPU                 | Kitchen                          |
| Ready Queue         | Order Queue                      |
| Context Switch      | Switching between orders         |
| Waiting Time        | Time order waits to start        |
| Turnaround Time     | Total time from order to ready   |
| Priority            | Order urgency / VIP status       |

## Project Structure

```
cpu-scheduling-food-simulator/
│
├── scheduler_engine/          # Core scheduling algorithms
│   ├── __init__.py
│   ├── order.py              # Order (Process) dataclass
│   ├── fcfs.py               # First Come First Served
│   ├── sjf.py                # Shortest Job First / SRTF
│   ├── priority.py           # Priority Scheduling
│   └── round_robin.py        # Round Robin
│
├── metrics/                   # Performance measurement
│   ├── __init__.py
│   └── performance.py        # Metrics calculator & comparator
│
├── visualization/             # Output visualization
│   ├── __init__.py
│   ├── gantt_chart.py        # ASCII Gantt charts
│   └── dashboard.py          # Combined dashboard view
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_schedulers.py
│
├── main.py                    # Main entry point
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required

### Running the Simulator

**Demo mode** — runs all 5 algorithms on sample orders and prints a comparison:
```bash
python main.py
```

**Interactive mode** — enter your own orders and choose an algorithm:
```bash
python main.py --interactive
```

### Running Tests

```bash
python -m unittest tests.test_schedulers -v
```

## Scheduling Algorithms

### 1. First Come First Served (FCFS)
- **Type**: Non-preemptive
- **How it works**: Orders are processed in strict arrival order
- **Pros**: Simple, no starvation
- **Cons**: Convoy effect — long orders can block short ones

### 2. Shortest Job First (SJF)
- **Type**: Non-preemptive
- **How it works**: Among available orders, the one with the shortest prep time goes next
- **Pros**: Minimises average waiting time
- **Cons**: Can starve long-running orders

### 3. Shortest Remaining Time First (SRTF)
- **Type**: Preemptive (preemptive SJF)
- **How it works**: A new arrival with a shorter remaining time preempts the current order
- **Pros**: Better average response time than SJF
- **Cons**: Higher context-switch overhead, possible starvation

### 4. Priority Scheduling
- **Type**: Non-preemptive (configurable to preemptive)
- **How it works**: Lower priority number = higher urgency; that order goes first
- **Pros**: Critical orders are served faster
- **Cons**: Low-priority orders may starve without ageing

### 5. Round Robin
- **Type**: Preemptive
- **How it works**: Each order gets a fixed time quantum; if not finished it rejoins the back of the queue
- **Pros**: Fair, responsive for all orders
- **Cons**: More context switches; quantum size affects performance

## Performance Metrics

Every algorithm run reports:

| Metric                  | Description                                      |
|-------------------------|--------------------------------------------------|
| Average Waiting Time    | Mean time orders spend in the queue              |
| Average Turnaround Time | Mean time from arrival to completion             |
| Average Response Time   | Mean time until an order is first touched        |
| Throughput              | Orders completed per time unit                   |
| CPU Utilization         | Percentage of time the kitchen is actively busy  |
| Max / Min Waiting Time  | Best and worst-case wait across all orders       |

## Example Output

```
╔════════════════════════════════════════════════════════════════════╗
║                   CPU Scheduling Food Simulator                    ║
╠════════════════════════════════════════════════════════════════════╣
║  Algorithm: FCFS                                                  ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────┐
│                           ORDER DETAILS                            │
├─────┬────────────┬─────────┬──────────┬──────────┬─────────┬───────┤
│ ID  │    Name    │ Arrival │ Prep Time│ Priority │ Wait    │ TAT   │
├─────┼────────────┼─────────┼──────────┼──────────┼─────────┼───────┤
│   1 │ Pizza      │       0 │        8 │        2 │       0 │     8 │
│   2 │ Burger     │       1 │        4 │        1 │       7 │    11 │
│   3 │ Salad      │       2 │        2 │        3 │      10 │    12 │
│   4 │ Pasta      │       3 │        6 │        2 │      11 │    17 │
│   5 │ Soup       │       4 │        3 │        4 │      16 │    19 │
└─────┴────────────┴─────────┴──────────┴──────────┴─────────┴───────┘

╔══════════════════════════════════════════════════════════════╗
║  Performance Metrics:                 FCFS                   ║
╠══════════════════════════════════════════════════════════════╣
║  Total Orders:                         5                     ║
║  Average Waiting Time:               8.80 time units         ║
║  Average Turnaround Time:           13.40 time units         ║
║  Average Response Time:              8.80 time units         ║
║  Throughput:                         0.2174 orders/time unit ║
║  CPU Utilization:                  100.00%                   ║
║  Max Waiting Time:                    16 time units          ║
║  Min Waiting Time:                     0 time units          ║
╚══════════════════════════════════════════════════════════════╝
```

## Notes

- The simulator handles **Windows terminal encoding** automatically — UTF-8 output is configured at startup so box-drawing characters render correctly on any platform.
- All algorithms use **deep copies** of order objects internally, so the original list is never mutated between runs.
- The SRTF and preemptive Priority schedulers simulate time in **1-unit steps** to correctly handle preemption.

## License

This project is open source and available under the MIT License.

## Educational Use

Designed to help students understand:
- CPU scheduling concepts and trade-offs
- Performance metrics (waiting time, turnaround time, throughput)
- Operating system fundamentals

Suitable for Operating Systems courses and self-study.

WORK DISTRIBUTION (MID-SEM) - 

scheduler_engine/

fcfs.py- AMBOY
order.py- GUPTA
priority.py - BAKSHI
round_robin.py - AYUSH
sjf.py - ADITYA 
