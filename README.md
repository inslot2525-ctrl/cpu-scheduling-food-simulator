# CPU Scheduling Food Simulator 🍕

A Python-based educational simulator that demonstrates CPU scheduling algorithms using food orders as an intuitive analogy.

## 🎯 Concept

This simulator helps understand Operating System CPU scheduling concepts by mapping them to a familiar context:

| CPU Scheduling Term | Food Simulator Equivalent |
|---------------------|---------------------------|
| Process             | Food Order                |
| Burst Time          | Preparation Time          |
| CPU                 | Kitchen                   |
| Ready Queue         | Order Queue               |
| Context Switch      | Switching between orders  |
| Waiting Time        | Time order waits to start |
| Turnaround Time     | Total time from order to ready |

## 🗂️ Project Structure

```
cpu-scheduling-food-simulator/
│
├── scheduler_engine/          # Core scheduling algorithms
│   ├── __init__.py
│   ├── order.py              # Order (Process) class
│   ├── fcfs.py               # First Come First Served
│   ├── sjf.py                # Shortest Job First / SRTF
│   ├── priority.py           # Priority Scheduling
│   └── round_robin.py        # Round Robin
│
├── metrics/                   # Performance measurement
│   ├── __init__.py
│   └── performance.py        # Metrics calculator
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

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required!

### Running the Simulator

**Demo Mode** (runs all algorithms with sample data):
```bash
python main.py
```

**Interactive Mode** (enter your own orders):
```bash
python main.py --interactive
```

### Running Tests

```bash
python -m pytest tests/
# or
python -m unittest tests.test_schedulers
```

## 📊 Scheduling Algorithms

### 1. First Come First Served (FCFS)
- **Type**: Non-preemptive
- **Description**: Orders are processed in the exact order they arrive
- **Pros**: Simple, fair (no starvation)
- **Cons**: Convoy effect (long orders delay short ones)

### 2. Shortest Job First (SJF)
- **Type**: Non-preemptive
- **Description**: Order with shortest preparation time goes first
- **Pros**: Optimal average waiting time
- **Cons**: May cause starvation for long orders

### 3. Shortest Remaining Time First (SRTF)
- **Type**: Preemptive
- **Description**: If a new order arrives with shorter remaining time, it preempts
- **Pros**: Better response time than SJF
- **Cons**: Higher overhead, possible starvation

### 4. Priority Scheduling
- **Type**: Configurable (preemptive/non-preemptive)
- **Description**: Orders with higher priority (lower number) go first
- **Pros**: Important orders get faster service
- **Cons**: Low priority orders may starve

### 5. Round Robin
- **Type**: Preemptive
- **Description**: Each order gets a fixed time quantum, then rotates
- **Pros**: Fair, good response time
- **Cons**: Higher overhead, context switching

## 📈 Performance Metrics

The simulator calculates:

- **Average Waiting Time**: Mean time orders spend waiting
- **Average Turnaround Time**: Mean time from arrival to completion
- **Average Response Time**: Mean time until first processing
- **Throughput**: Orders completed per time unit
- **CPU Utilization**: Percentage of time kitchen is busy

## 🎮 Example Output

```
╔══════════════════════════════════════════════════════════════╗
║  Performance Metrics: FCFS                                   ║
╠══════════════════════════════════════════════════════════════╣
║  Total Orders:                   5                           ║
║  Average Waiting Time:        8.40 time units                ║
║  Average Turnaround Time:    13.00 time units                ║
║  CPU Utilization:           100.00%                          ║
╚══════════════════════════════════════════════════════════════╝
```

## 🤝 Contributing

Feel free to:
- Add new scheduling algorithms
- Improve visualizations
- Add more metrics
- Enhance the interactive mode

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Educational Use

This simulator is designed for educational purposes to help students understand:
- CPU scheduling concepts
- Algorithm trade-offs
- Performance metrics
- Operating system fundamentals

Perfect for Operating Systems courses and self-study!
