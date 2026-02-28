"""
Priority Scheduling Algorithm.
Orders are processed based on priority level (lower number = higher priority).
"""
from typing import List, Tuple
from copy import deepcopy
from .order import Order


class PriorityScheduler:
    """
    Priority-based scheduler.
    Can be preemptive or non-preemptive.
    """
    
    def __init__(self, preemptive: bool = False):
        self.preemptive = preemptive
        self.name = "Preemptive Priority" if preemptive else "Non-Preemptive Priority"
    
    def schedule(self, orders: List[Order]) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
        """
        Schedule orders using Priority algorithm.
        
        Args:
            orders: List of Order objects to schedule
            
        Returns:
            Tuple of (completed_orders, gantt_data)
        """
        if not orders:
            return [], []
        
        # Create deep copies to avoid modifying original orders
        work_orders = deepcopy(orders)
        for order in work_orders:
            order.remaining_time = order.preparation_time
        
        gantt_data = []
        completed = []
        current_time = 0
        ready_queue = []
        last_order_id = None
        segment_start = 0
        
        while len(completed) < len(work_orders):
            # Add newly arrived orders to ready queue
            for order in work_orders:
                if order.arrival_time <= current_time and order not in ready_queue and order not in completed:
                    ready_queue.append(order)
            
            if not ready_queue:
                current_time += 1
                continue
            
            # Select order with highest priority (lowest priority number)
            ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
            selected = ready_queue[0]
            
            if self.preemptive:
                # Process for 1 time unit
                if last_order_id != selected.order_id:
                    if last_order_id is not None:
                        gantt_data.append((last_order_id, segment_start, current_time))
                    segment_start = current_time
                    if selected.start_time is None:
                        selected.start_time = current_time
                
                selected.remaining_time -= 1
                current_time += 1
                last_order_id = selected.order_id
                
                if selected.remaining_time == 0:
                    selected.completion_time = current_time
                    selected.calculate_metrics()
                    completed.append(selected)
                    ready_queue.remove(selected)
                    gantt_data.append((selected.order_id, segment_start, current_time))
                    last_order_id = None
            else:
                # Non-preemptive: process entire order
                selected.start_time = current_time
                current_time += selected.preparation_time
                selected.completion_time = current_time
                selected.remaining_time = 0
                selected.calculate_metrics()
                completed.append(selected)
                ready_queue.remove(selected)
                gantt_data.append((selected.order_id, selected.start_time, selected.completion_time))
        
        return completed, gantt_data


def run_priority(orders: List[Order], preemptive: bool = False) -> Tuple[List[Order], List[Tuple[int, int, int]]]:
    """Convenience function to run Priority scheduling."""
    scheduler = PriorityScheduler(preemptive=preemptive)
    return scheduler.schedule(orders)
