"""
First Come First Served (FCFS) Scheduling Algorithm.
Orders are processed in the order they arrive - like a traditional queue.
"""
from typing import List, Tuple
from .order import Order


class FCFSScheduler:
    """
    First Come First Served scheduler.
    Non-preemptive: once an order starts, it runs to completion.
    """
    
    def __init__(self):
        self.name = "First Come First Served (FCFS)"
    
    def schedule(self, orders: List[Order]) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
        """
        Schedule orders using FCFS algorithm.
        
        Args:
            orders: List of Order objects to schedule
            
        Returns:
            Tuple of (completed_orders, gantt_data)
            - completed_orders: Orders with calculated metrics
            - gantt_data: List of (order_id, start_time, end_time) for Gantt chart
        """
        if not orders:
            return [], []
        
        # Sort by arrival time
        sorted_orders = sorted(orders, key=lambda x: (x.arrival_time, x.order_id))
        gantt_data = []
        current_time = 0
        
        for order in sorted_orders:
            # If CPU is idle, jump to the arrival time of next order
            if current_time < order.arrival_time:
                current_time = order.arrival_time
            
            # Set start time
            order.start_time = current_time
            
            # Process the order
            current_time += order.preparation_time
            
            # Set completion time
            order.completion_time = current_time
            
            # Calculate metrics
            order.calculate_metrics()
            
            # Record for Gantt chart
            gantt_data.append((order.order_id, order.start_time, order.completion_time))
        
        return sorted_orders, gantt_data


def run_fcfs(orders: List[Order]) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
    """Convenience function to run FCFS scheduling."""
    scheduler = FCFSScheduler()
    return scheduler.schedule(orders)
