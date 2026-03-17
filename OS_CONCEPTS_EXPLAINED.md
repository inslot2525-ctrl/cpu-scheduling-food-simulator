# OS Concepts & Code Explanation — CPU Scheduling Food Simulator

This document walks through every file in the project, lists the Operating System concepts used, explains those concepts, and explains what the code does.

---

## Table of Contents

1. [scheduler_engine/order.py](#1-scheduler_engineorderpy)
2. [scheduler_engine/fcfs.py](#2-scheduler_enginefcfspy) — AMBOY
3. [scheduler_engine/sjf.py](#3-scheduler_enginesjfpy) — ADITYA
4. [scheduler_engine/priority.py](#4-scheduler_engineprioritypy) — BAKSHI
5. [scheduler_engine/round_robin.py](#5-scheduler_engineround_robinpy) — AYUSH
6. [metrics/performance.py](#6-metricsperformancepy)
7. [visualization/gantt_chart.py](#7-visualizationgantt_chartpy)
8. [visualization/dashboard.py](#8-visualizationdashboardpy)
9. [tests/test_schedulers.py](#9-teststest_schedulerspy)
10. [main.py](#10-mainpy)
11. [Work Distribution](#work-distribution-mid-sem)

---

## 1. `scheduler_engine/order.py`

**Author: GUPTA**

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Process Control Block (PCB)** | In a real OS, every process has a PCB — a data structure that stores its state: ID, arrival time, burst time, priority, and timing information. The `Order` class is a direct simulation of a PCB. |
| **Burst Time** | The total CPU time a process needs to finish. Here it is `preparation_time`. |
| **Arrival Time** | The moment a process enters the ready queue. Same field name used here. |
| **Priority** | An integer attached to a process that schedulers use to decide execution order. Lower number = higher urgency (common OS convention). |
| **Remaining Time** | Used specifically in preemptive algorithms. Tracks how much CPU time is still needed after partial execution. Without this, preemptive scheduling cannot resume interrupted processes correctly. |
| **Waiting Time** | The time a process spends sitting in the ready queue before the CPU picks it up. Formula: `Turnaround Time − Burst Time`. |
| **Turnaround Time** | Total elapsed time from when a process arrives to when it finishes. Formula: `Completion Time − Arrival Time`. |

### Code Explanation

```python
@dataclass
class Order:
    order_id: int
    name: str
    arrival_time: int
    preparation_time: int       # = Burst Time
    priority: int = 0
    remaining_time: Optional[int] = None   # for preemptive algorithms
    start_time: Optional[int] = None
    completion_time: Optional[int] = None
    waiting_time: Optional[int] = None
    turnaround_time: Optional[int] = None
```

- `@dataclass` auto-generates `__init__`, so each field becomes a constructor argument.
- `__post_init__` runs right after `__init__`. It sets `remaining_time = preparation_time` because at the start, remaining work equals total work.
- `calculate_metrics()` computes waiting time and turnaround time once `completion_time` is known. This mirrors how an OS kernel records process statistics when a process exits.

---

## 2. `scheduler_engine/fcfs.py`

**Author: AMBOY**

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **First Come First Served (FCFS)** | The simplest non-preemptive scheduling algorithm. The CPU services processes strictly in the order they arrive — just like a real queue at a counter. |
| **Non-preemptive Scheduling** | Once a process starts on the CPU, it runs until it voluntarily completes. No other process can interrupt it midway. |
| **Ready Queue** | A queue of processes that have arrived and are waiting for CPU time. FCFS serves them front-to-back. |
| **Convoy Effect** | A key weakness of FCFS. If one long process arrives early, all shorter processes behind it must wait, causing high average waiting times. |
| **CPU Idle Time** | When no process is available at a given moment, the CPU sits idle. The code handles this by advancing `current_time` to the next arrival. |
| **Gantt Chart Data** | Encodes the CPU timeline as `(process_id, start, end)` segments for visualisation. |

### Code Explanation

```python
sorted_orders = sorted(orders, key=lambda x: (x.arrival_time, x.order_id))
```
Sorts all orders by arrival time. Ties broken by ID, matching the FCFS rule.

```python
if current_time < order.arrival_time:
    current_time = order.arrival_time
```
Handles CPU idle gaps — if the next process hasn't arrived yet, time jumps forward.

```python
order.start_time = current_time
current_time += order.preparation_time
order.completion_time = current_time
order.calculate_metrics()
gantt_data.append((order.order_id, order.start_time, order.completion_time))
```
The heart of FCFS: set start, run to completion (add burst time), record finish, then log the segment for the Gantt chart. The loop moves through every order exactly once — O(n) execution.

---

## 3. `scheduler_engine/sjf.py`

**Author: ADITYA**

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Shortest Job First (SJF)** | Non-preemptive algorithm. Among all processes currently in the ready queue, the one with the smallest burst time is picked next. Provably optimal for minimising average waiting time among non-preemptive algorithms. |
| **Shortest Remaining Time First (SRTF)** | The preemptive version of SJF. When a new process arrives, if its remaining burst time is less than what the current process still needs, the current process is preempted (paused) and the shorter one takes over. |
| **Preemption** | The OS forcibly stops a running process mid-execution to give the CPU to a higher-priority (or shorter) process. Requires saving the process state so it can be resumed later. |
| **Context Switch** | Every time SRTF preempts a process, a context switch occurs — the CPU saves the current process state and loads the next. The code records each such switch as a separate Gantt segment. |
| **Starvation** | A possible side effect of SJF/SRTF. Long processes may wait indefinitely if short processes keep arriving. Not addressed in this simulator (no ageing), but documented in the README. |
| **Ready Queue** | Dynamically populated as new orders arrive at each time tick. |
| **Deep Copy** | To prevent the original order list from being mutated across multiple algorithm runs. |

### Code Explanation

**Non-preemptive path:**
```python
ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
selected = ready_queue[0]
selected.start_time = current_time
current_time += selected.preparation_time
```
At each decision point, sort the ready queue by burst time and pick the shortest. Run it fully to completion. Simple and clean.

**Preemptive path (SRTF):**
```python
# Process for exactly 1 time unit at a time
selected.remaining_time -= 1
current_time += 1
```
Time advances in 1-unit steps. After each step, the ready queue is re-sorted. If a newly arrived order has less remaining time than the current one, it becomes `selected[0]` on the next iteration — this is the preemption. The old process's progress is preserved in its `remaining_time`.

```python
if last_order_id != selected.order_id:
    gantt_data.append((last_order_id, segment_start, current_time))
    segment_start = current_time
```
Detects context switches: whenever the selected process changes, close the previous Gantt segment and open a new one.

---

## 4. `scheduler_engine/priority.py`

**Author: BAKSHI**

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Priority Scheduling** | Each process is assigned a priority number. The CPU always runs the highest-priority ready process. In this simulator, a **lower number means higher priority** (common in real OSes like Linux `nice` values). |
| **Non-preemptive Priority** | The current process runs to completion even if a higher-priority process arrives. The higher-priority one is served next. |
| **Preemptive Priority** | If a higher-priority process arrives while a lower-priority one is running, the CPU immediately switches. The interrupted process resumes later. |
| **Starvation** | Low-priority processes may never run if high-priority ones keep arriving. Real OSes use **ageing** (gradually boosting priority over time) to prevent this — not implemented here, but the architecture supports it. |
| **Context Switch** | Same mechanism as SRTF. Tracked via `last_order_id` and `segment_start`. |
| **Ready Queue** | All processes that have arrived and not yet completed. Sorted by `(priority, arrival_time)` at every scheduling decision. |
| **Deep Copy** | Protects the original order list from mutation. |

### Code Explanation

The structure is nearly identical to `sjf.py` — the only difference is the sort key:

```python
# SJF sorts by:
ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))

# Priority sorts by:
ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
```

This single change in selection criterion is the entire difference between SJF and Priority Scheduling — a clean demonstration of how the scheduler's decision policy is the only variable.

The non-preemptive branch runs the selected order fully:
```python
selected.start_time = current_time
current_time += selected.preparation_time
selected.completion_time = current_time
selected.calculate_metrics()
```

The preemptive branch ticks one unit at a time, records context switches, and checks for preemption on every tick — the same time-slicing loop used in SRTF.

---

## 5. `scheduler_engine/round_robin.py`

**Author: AYUSH**

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Round Robin (RR)** | Each process gets a fixed slice of CPU time called a **time quantum**. If it doesn't finish within that quantum, it's paused and added to the back of the queue. This repeats cyclically until all processes complete. |
| **Time Quantum** | The maximum CPU time a process can use in one turn. Choosing a good quantum is critical — too small causes excessive context switches; too large degrades to FCFS. |
| **Preemptive Scheduling** | RR is inherently preemptive. After each quantum, the OS forces a context switch regardless of how much work remains. |
| **Context Switch Overhead** | Every time a process is swapped out after its quantum, the OS must save its registers and load the next process's state. RR has the most context switches among all the algorithms here. |
| **Circular Queue / FIFO Queue** | The ready queue in RR is a FIFO: new arrivals and preempted processes join the **back**, and the scheduler always picks from the **front**. This is implemented with Python's `collections.deque`. |
| **Fairness** | RR is the fairest scheduler — every process gets equal CPU time in turns. No process can monopolise the CPU beyond one quantum. |
| **Response Time** | RR typically gives the best average response time (time until first CPU touch) because processes don't wait for long jobs ahead to fully complete. |
| **Deep Copy** | Orders are deep-copied so the original list is unchanged across algorithm runs. |

### Code Explanation

```python
from collections import deque
ready_queue = deque()
```
`deque` is used for O(1) `append` (right) and `popleft` (left) — exactly the operations needed for a FIFO queue.

```python
exec_time = min(self.time_quantum, current_order.remaining_time)
current_time += exec_time
current_order.remaining_time -= exec_time
```
Executes either a full quantum, or whatever is left if less than a quantum remains. This correctly handles the last partial slice.

```python
# Add newly arrived orders AFTER advancing time
while order_index < len(work_orders) and work_orders[order_index].arrival_time <= current_time:
    ready_queue.append(work_orders[order_index])
    order_index += 1
```
New arrivals are added to the queue *after* the current quantum executes. This ensures arrivals during a quantum are queued behind the currently executing process — correct RR behaviour.

```python
if current_order.remaining_time == 0:
    current_order.completion_time = current_time
    current_order.calculate_metrics()
    completed.append(current_order)
else:
    ready_queue.append(current_order)   # re-queue at the back
```
If done, record completion. Otherwise, push back to the end of the queue for its next turn.

---

## 6. `metrics/performance.py`

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Waiting Time** | Time a process spends in the ready queue. Lower is better. Formula per process: `turnaround_time − burst_time`. |
| **Turnaround Time** | Total lifecycle time of a process. Formula: `completion_time − arrival_time`. The key end-to-end metric. |
| **Response Time** | Time from arrival until the process first gets the CPU. Important for interactive systems. Formula: `start_time − arrival_time`. |
| **Throughput** | Number of processes completed per unit time. Measures how productive the CPU is. Formula: `total_processes / makespan`. |
| **CPU Utilisation** | Percentage of time the CPU is busy (not idle). Formula: `total_burst_time / makespan × 100`. A good scheduler maximises this. |
| **Makespan** | The total time from the first arrival to the last completion — the overall schedule length. |

### Code Explanation

```python
def _calculate_metrics(self) -> Dict[str, Any]:
    waiting_times = [o.waiting_time for o in self.orders if o.waiting_time is not None]
    turnaround_times = [o.turnaround_time for o in self.orders if o.turnaround_time is not None]
    response_times = [o.start_time - o.arrival_time for o in self.orders if o.start_time is not None]
```
Collects per-process metrics into lists, then computes averages. `None` guards handle cases where a process was never started (defensive coding).

```python
makespan = last_completion - first_arrival
cpu_utilization = (total_prep_time / makespan * 100)
```
`makespan` is the denominator for both throughput and CPU utilisation. If there are idle gaps between processes, `makespan > total_prep_time`, pushing utilisation below 100%.

`get_summary()` formats everything into the bordered box display seen in the output. `compare_with()` and `compare_algorithms()` produce side-by-side tables to help evaluate which algorithm performs best for a given workload.

---

## 7. `visualization/gantt_chart.py`

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Gantt Chart** | A standard tool in OS education to visualise CPU scheduling. Time runs on the X-axis; each row represents a process. Filled blocks show when each process was on the CPU. |
| **Timeline / Schedule Representation** | The `gantt_data` list of `(order_id, start, end)` tuples is the canonical representation of a CPU schedule — identical to what an OS profiler would record. |
| **Context Switch Visibility** | Each separate segment in the Gantt chart represents one CPU burst. Multiple segments for the same process indicate preemptions (context switches occurred between them). |

### Code Explanation

```python
scale = max_width / time_range
```
Scales the entire timeline to fit within `max_width` characters. Each character represents `time_range / max_width` time units.

```python
for start, end in segments:
    start_pos = int((start - min_time) * scale)
    end_pos   = int((end   - min_time) * scale)
    for i in range(start_pos, end_pos):
        line[i] = '█'
```
Converts time coordinates to character positions and fills them with block characters — producing the visual bars in the ASCII chart.

`generate_detailed()` produces a second, tabular view showing exact start/end times and a proportional bar (`▓` characters) per segment — useful for seeing precise timings that the scaled chart may compress.

---

## 8. `visualization/dashboard.py`

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Scheduling Algorithm Comparison** | A key activity in OS analysis: running multiple schedulers on the same workload and comparing their metrics to determine which fits the use-case best. |
| **Performance Metrics Display** | Aggregates waiting time, turnaround time, response time, throughput, and CPU utilisation into a unified view — matching what OS performance profiling tools report. |
| **Algorithm Selection Trade-offs** | The "Best Performers" section explicitly shows which algorithm wins each metric, reflecting the core OS lesson that no single algorithm is optimal for all metrics simultaneously. |

### Code Explanation

`Dashboard.display()` orchestrates the full output for one algorithm run:
1. Prints a header box with the algorithm name.
2. Calls `_generate_order_table()` for the per-process metrics table.
3. Creates a `GanttChart`, calls both `generate()` (visual) and `generate_detailed()` (tabular).
4. Instantiates `PerformanceMetrics` and calls `get_summary()`.

`compare_algorithms()` iterates over a dictionary of `{name: (orders, gantt_data)}` pairs:
- Renders a mini Gantt chart per algorithm.
- Builds a side-by-side metrics table.
- Identifies the best-performing algorithm per metric using `min()` / `max()` over the values dictionary.

---

## 9. `tests/test_schedulers.py`

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Correctness Verification** | Unit tests validate that each algorithm produces the mathematically correct completion times, a critical requirement when OS schedulers are expected to behave deterministically. |
| **Preemption Testing** | `test_preemptive_sjf` verifies that Salad (arriving at t=1 with burst=2) correctly preempts Pizza (started at t=0 with burst=5) and completes at t=3 — confirming SRTF preemption logic works. |
| **Priority Correctness** | `test_priority_scheduling` checks that the process with the lowest priority number (VIP Steak, priority=1) is always scheduled first. |
| **Round Robin Interleaving** | `test_round_robin_quantum_2` asserts that the Gantt chart has more than 2 segments for 2 processes — confirming time-slicing (interleaving) actually happened. |

### Code Explanation

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```
Adds the project root to Python's module search path so imports work regardless of where the tests are invoked from.

Each test class corresponds to one scheduler. Tests create minimal `Order` objects, run the scheduler, and assert on completion times or ordering. The `TestOrder` class tests `calculate_metrics()` directly — ensuring the fundamental formula (`turnaround = completion − arrival`, `waiting = turnaround − burst`) is correct before testing the algorithms that depend on it.

---

## 10. `main.py`

### OS Concepts Used

| Concept | Explanation |
|---|---|
| **Scheduler Dispatcher** | `main.py` acts like an OS dispatcher — it takes a workload (the 5 orders) and routes it through each scheduling algorithm, collecting results. |
| **Process Workload** | `create_sample_orders()` defines the benchmark workload: 5 processes with different arrival times, burst times, and priorities — a standard OS scheduling test case. |
| **Deep Copy for Isolation** | Each algorithm call receives a fresh `create_sample_orders()` (or `deepcopy(orders)` in interactive mode). This mirrors how an OS would apply different scheduling policies to the same process set independently. |
| **Interactive vs Batch Mode** | `sys.argv` checking mirrors how OS utilities support both scripted (batch) and user-driven (interactive) operation. |
| **Encoding Configuration** | `sys.stdout.reconfigure(encoding='utf-8')` on Windows ensures box-drawing characters (used in Gantt charts and tables) render correctly — a practical systems-programming concern. |

### Code Explanation

```python
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
```
Windows terminals default to `cp1252` encoding, which cannot render Unicode box-drawing characters. This line reconfigures stdout to UTF-8 at startup.

```python
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        run_simulation()
```
Standard Python entry-point pattern. `run_simulation()` runs all 5 algorithms in sequence on the sample workload and prints a comparison. `interactive_mode()` accepts user input for custom orders and algorithm choice.

`run_simulation()` stores results in `all_results = {}` and passes the entire dictionary to `Dashboard.compare_algorithms()` — producing the final side-by-side comparison table.

---

## Summary: OS Concepts Across the Whole Project

| OS Concept | Where It Appears |
|---|---|
| Process / PCB | `order.py` — the `Order` dataclass |
| Burst Time | All scheduler files, `order.py` |
| Arrival Time | All scheduler files |
| Ready Queue | `fcfs.py`, `sjf.py`, `priority.py`, `round_robin.py` |
| Non-preemptive Scheduling | `fcfs.py`, non-preemptive branches of `sjf.py` and `priority.py` |
| Preemptive Scheduling / Preemption | `sjf.py` (SRTF), `priority.py` (preemptive), `round_robin.py` |
| Context Switch | `sjf.py`, `priority.py`, `round_robin.py` — recorded as Gantt segments |
| Time Quantum | `round_robin.py` |
| Priority | `priority.py`, `order.py` |
| Remaining Time | `sjf.py`, `priority.py`, `round_robin.py` |
| Waiting Time | `order.py` (formula), `metrics/performance.py` (aggregation) |
| Turnaround Time | `order.py` (formula), `metrics/performance.py` (aggregation) |
| Response Time | `metrics/performance.py` |
| CPU Utilisation | `metrics/performance.py` |
| Throughput | `metrics/performance.py` |
| Gantt Chart | `visualization/gantt_chart.py`, `visualization/dashboard.py` |
| Starvation | Documented in README; relevant to SJF, SRTF, Priority |
| Convoy Effect | Documented in README; relevant to FCFS |
| Fairness | `round_robin.py` — RR is the only fair algorithm here |

---

## Work Distribution (MID-SEM)

| File | Author |
|---|---|
| `scheduler_engine/fcfs.py` | AMBOY |
| `scheduler_engine/order.py` | GUPTA |
| `scheduler_engine/priority.py` | BAKSHI |
| `scheduler_engine/round_robin.py` | AYUSH |
| `scheduler_engine/sjf.py` | ADITYA |
