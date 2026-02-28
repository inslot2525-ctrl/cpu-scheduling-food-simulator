"""
Unit tests for scheduling algorithms.
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler_engine.order import Order
from scheduler_engine.fcfs import run_fcfs
from scheduler_engine.sjf import run_sjf
from scheduler_engine.priority import run_priority
from scheduler_engine.round_robin import run_round_robin


class TestOrder(unittest.TestCase):
    """Test Order class functionality."""
    
    def test_order_creation(self):
        order = Order(1, "Pizza", 0, 5, priority=2)
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.name, "Pizza")
        self.assertEqual(order.arrival_time, 0)
        self.assertEqual(order.preparation_time, 5)
        self.assertEqual(order.priority, 2)
        self.assertEqual(order.remaining_time, 5)
    
    def test_calculate_metrics(self):
        order = Order(1, "Burger", 0, 5)
        order.start_time = 0
        order.completion_time = 5
        order.calculate_metrics()
        self.assertEqual(order.waiting_time, 0)
        self.assertEqual(order.turnaround_time, 5)


class TestFCFS(unittest.TestCase):
    """Test FCFS scheduling algorithm."""
    
    def test_simple_fcfs(self):
        orders = [
            Order(1, "Pizza", 0, 5),
            Order(2, "Burger", 1, 3),
            Order(3, "Salad", 2, 2)
        ]
        completed, gantt = run_fcfs(orders)
        
        # First order should complete at time 5
        self.assertEqual(completed[0].completion_time, 5)
        # Second order starts at 5, completes at 8
        self.assertEqual(completed[1].completion_time, 8)
        # Third order starts at 8, completes at 10
        self.assertEqual(completed[2].completion_time, 10)
    
    def test_empty_orders(self):
        completed, gantt = run_fcfs([])
        self.assertEqual(len(completed), 0)
        self.assertEqual(len(gantt), 0)


class TestSJF(unittest.TestCase):
    """Test SJF scheduling algorithm."""
    
    def test_non_preemptive_sjf(self):
        orders = [
            Order(1, "Pizza", 0, 5),
            Order(2, "Salad", 0, 2),
            Order(3, "Burger", 0, 3)
        ]
        completed, gantt = run_sjf(orders, preemptive=False)
        
        # Orders should complete in order: Salad(2), Burger(5), Pizza(10)
        completion_order = [o.order_id for o in sorted(completed, key=lambda x: x.completion_time)]
        self.assertEqual(completion_order, [2, 3, 1])
    
    def test_preemptive_sjf(self):
        orders = [
            Order(1, "Pizza", 0, 5),
            Order(2, "Salad", 1, 2)
        ]
        completed, gantt = run_sjf(orders, preemptive=True)
        
        # Salad arrives at t=1 with shorter time, should preempt Pizza
        salad = next(o for o in completed if o.order_id == 2)
        self.assertEqual(salad.completion_time, 3)  # 1 + 2 = 3


class TestPriority(unittest.TestCase):
    """Test Priority scheduling algorithm."""
    
    def test_priority_scheduling(self):
        orders = [
            Order(1, "Pizza", 0, 5, priority=3),
            Order(2, "VIP Steak", 0, 4, priority=1),
            Order(3, "Burger", 0, 3, priority=2)
        ]
        completed, gantt = run_priority(orders, preemptive=False)
        
        # VIP Steak (priority 1) should be first
        first_completed = min(completed, key=lambda x: x.completion_time)
        self.assertEqual(first_completed.order_id, 2)


class TestRoundRobin(unittest.TestCase):
    """Test Round Robin scheduling algorithm."""
    
    def test_round_robin_quantum_2(self):
        orders = [
            Order(1, "Pizza", 0, 5),
            Order(2, "Burger", 0, 3)
        ]
        completed, gantt = run_round_robin(orders, time_quantum=2)
        
        # Both orders should be completed
        self.assertEqual(len(completed), 2)
        
        # Check that work was interleaved
        self.assertTrue(len(gantt) > 2)
    
    def test_round_robin_single_order(self):
        orders = [Order(1, "Pizza", 0, 3)]
        completed, gantt = run_round_robin(orders, time_quantum=2)
        
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].completion_time, 3)


if __name__ == '__main__':
    unittest.main()
