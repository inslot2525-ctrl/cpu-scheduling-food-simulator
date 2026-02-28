"""
Order class representing a food order in the CPU scheduling simulator.
Each order is analogous to a process in CPU scheduling.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """
    Represents a food order with scheduling attributes.
    
    Attributes:
        order_id: Unique identifier for the order
        name: Name of the food item
        arrival_time: Time when the order was placed
        preparation_time: Time required to prepare the order (burst time)
        priority: Priority level (lower number = higher priority)
        remaining_time: Time remaining for preparation (used in preemptive algorithms)
        start_time: Time when preparation started
        completion_time: Time when preparation completed
        waiting_time: Time spent waiting before preparation started
        turnaround_time: Total time from arrival to completion
    """
    order_id: int
    name: str
    arrival_time: int
    preparation_time: int
    priority: int = 0
    remaining_time: Optional[int] = None
    start_time: Optional[int] = None
    completion_time: Optional[int] = None
    waiting_time: Optional[int] = None
    turnaround_time: Optional[int] = None

    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.preparation_time

    def calculate_metrics(self):
        """Calculate waiting time and turnaround time after completion."""
        if self.completion_time is not None and self.arrival_time is not None:
            self.turnaround_time = self.completion_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.preparation_time

    def __repr__(self):
        return f"Order({self.order_id}, '{self.name}', arrival={self.arrival_time}, prep={self.preparation_time})"
