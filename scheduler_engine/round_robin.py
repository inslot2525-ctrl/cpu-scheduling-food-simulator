"""
Round Robin Scheduling Algorithm.
Each order gets a fixed time quantum, then moves to the back of the queue.
"""
from typing import List, Tuple
from copy import deepcopy
from collections import deque
from .order import Order


class RoundRobinScheduler:
    """
    Round Robin scheduler with configurable time quantum.
    Always preemptive.
    """
    
    def __init__(self, time_quantum: int = 2):
        self.time_quantum = time_quantum
        self.name = f"Round Robin (quantum={time_quantum})"
    
    def schedule(self, orders: List[Order]) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
        """
        Schedule orders using Round Robin algorithm.
        
        Args:
            orders: List of Order objects to schedule
            
        Returns:
            Tuple of (completed_orders, gantt_data)
        """
        if not orders:
            return [], []
        
        # Create deep copies and sort by arrival time
        work_orders = deepcopy(orders)
        work_orders.sort(key=lambda x: x.arrival_time)
        for order in work_orders:
            order.remaining_time = order.preparation_time
        
        gantt_data = []
        completed = []
        ready_queue = deque()
        current_time = 0
        order_index = 0
        
        # Add first order(s) that arrive at time 0
        while order_index < len(work_orders) and work_orders[order_index].arrival_time <= current_time:
            ready_queue.append(work_orders[order_index])
            order_index += 1
        
        while ready_queue or order_index < len(work_orders):
            if not ready_queue:
                # No orders ready, jump to next arrival
                current_time = work_orders[order_index].arrival_time
                while order_index < len(work_orders) and work_orders[order_index].arrival_time <= current_time:
                    ready_queue.append(work_orders[order_index])
                    order_index += 1
            
            # Get next order from queue
            current_order = ready_queue.popleft()
            
            # Record start time if first time processing
            if current_order.start_time is None:
                current_order.start_time = current_time
            
            # Calculate execution time for this quantum
            exec_time = min(self.time_quantum, current_order.remaining_time)
            
            # Execute
            segment_start = current_time
            current_time += exec_time
            current_order.remaining_time -= exec_time
            
            # Add to Gantt chart
            gantt_data.append((current_order.order_id, segment_start, current_time))
            
            # Add newly arrived orders to queue
            while order_index < len(work_orders) and work_orders[order_index].arrival_time <= current_time:
                ready_queue.append(work_orders[order_index])
                order_index += 1
            
            # Check if order is complete
            if current_order.remaining_time == 0:
                current_order.completion_time = current_time
                current_order.calculate_metrics()
                completed.append(current_order)
            else:
                # Put back at end of queue
                ready_queue.append(current_order)
        
        return completed, gantt_data


def run_round_robin(orders: List[Order], time_quantum: int = 2) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
    """Convenience function to run Round Robin scheduling."""
    scheduler = RoundRobinScheduler(time_quantum=time_quantum)
    return scheduler.schedule(orders)
