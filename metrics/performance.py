"""
Performance Metrics Calculator for CPU Scheduling Simulation.
Calculates various metrics to evaluate scheduling algorithm efficiency.
"""
from typing import List, Dict, Any
from scheduler_engine.order import Order


class PerformanceMetrics:
    """
    Calculates and stores performance metrics for scheduling algorithms.
    """
    
    def __init__(self, orders: List[Order], algorithm_name: str = ""):
        self.orders = orders
        self.algorithm_name = algorithm_name
        self.metrics = self._calculate_metrics()
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all performance metrics."""
        if not self.orders:
            return {
                'total_orders': 0,
                'avg_waiting_time': 0,
                'avg_turnaround_time': 0,
                'avg_response_time': 0,
                'throughput': 0,
                'cpu_utilization': 0,
                'max_waiting_time': 0,
                'min_waiting_time': 0
            }
        
        waiting_times = [o.waiting_time for o in self.orders if o.waiting_time is not None]
        turnaround_times = [o.turnaround_time for o in self.orders if o.turnaround_time is not None]
        response_times = [o.start_time - o.arrival_time for o in self.orders if o.start_time is not None]
        
        # Calculate makespan (total time from first arrival to last completion)
        first_arrival = min(o.arrival_time for o in self.orders)
        last_completion = max(o.completion_time for o in self.orders if o.completion_time is not None)
        makespan = last_completion - first_arrival
        
        # Calculate total preparation time (busy time)
        total_prep_time = sum(o.preparation_time for o in self.orders)
        
        return {
            'total_orders': len(self.orders),
            'avg_waiting_time': sum(waiting_times) / len(waiting_times) if waiting_times else 0,
            'avg_turnaround_time': sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0,
            'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
            'throughput': len(self.orders) / makespan if makespan > 0 else 0,
            'cpu_utilization': (total_prep_time / makespan * 100) if makespan > 0 else 0,
            'max_waiting_time': max(waiting_times) if waiting_times else 0,
            'min_waiting_time': min(waiting_times) if waiting_times else 0,
            'makespan': makespan,
            'total_preparation_time': total_prep_time
        }
    
    def get_summary(self) -> str:
        """Get a formatted summary of all metrics."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  Performance Metrics: {self.algorithm_name:^37} ║
╠══════════════════════════════════════════════════════════════╣
║  Total Orders:              {self.metrics['total_orders']:>10}                     ║
║  Average Waiting Time:      {self.metrics['avg_waiting_time']:>10.2f} time units         ║
║  Average Turnaround Time:   {self.metrics['avg_turnaround_time']:>10.2f} time units         ║
║  Average Response Time:     {self.metrics['avg_response_time']:>10.2f} time units         ║
║  Throughput:                {self.metrics['throughput']:>10.4f} orders/time unit   ║
║  CPU Utilization:           {self.metrics['cpu_utilization']:>10.2f}%                    ║
║  Max Waiting Time:          {self.metrics['max_waiting_time']:>10} time units         ║
║  Min Waiting Time:          {self.metrics['min_waiting_time']:>10} time units         ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    def compare_with(self, other: 'PerformanceMetrics') -> str:
        """Compare metrics with another algorithm's results."""
        comparison = f"\n{'Metric':<25} {self.algorithm_name:<15} {other.algorithm_name:<15} {'Better':<10}\n"
        comparison += "─" * 65 + "\n"
        
        metrics_to_compare = [
            ('Avg Waiting Time', 'avg_waiting_time', 'lower'),
            ('Avg Turnaround Time', 'avg_turnaround_time', 'lower'),
            ('Avg Response Time', 'avg_response_time', 'lower'),
            ('Throughput', 'throughput', 'higher'),
            ('CPU Utilization', 'cpu_utilization', 'higher')
        ]
        
        for label, key, better in metrics_to_compare:
            val1 = self.metrics[key]
            val2 = other.metrics[key]
            
            if better == 'lower':
                winner = self.algorithm_name if val1 < val2 else other.algorithm_name
            else:
                winner = self.algorithm_name if val1 > val2 else other.algorithm_name
            
            if val1 == val2:
                winner = "Tie"
            
            comparison += f"{label:<25} {val1:<15.2f} {val2:<15.2f} {winner:<10}\n"
        
        return comparison


def compare_algorithms(results: Dict[str, List[Order]]) -> str:
    """
    Compare multiple scheduling algorithms.
    
    Args:
        results: Dictionary mapping algorithm names to their completed orders
        
    Returns:
        Formatted comparison string
    """
    metrics_list = []
    for name, orders in results.items():
        metrics_list.append(PerformanceMetrics(orders, name))
    
    output = "\n" + "=" * 70 + "\n"
    output += "ALGORITHM COMPARISON\n"
    output += "=" * 70 + "\n"
    
    # Header
    headers = ['Metric'] + [m.algorithm_name[:12] for m in metrics_list]
    output += f"{headers[0]:<20}"
    for h in headers[1:]:
        output += f" {h:>12}"
    output += "\n" + "─" * 70 + "\n"
    
    # Metrics
    metric_names = [
        ('Avg Wait', 'avg_waiting_time'),
        ('Avg Turnaround', 'avg_turnaround_time'),
        ('Avg Response', 'avg_response_time'),
        ('Throughput', 'throughput'),
        ('CPU Util %', 'cpu_utilization')
    ]
    
    for label, key in metric_names:
        output += f"{label:<20}"
        for m in metrics_list:
            output += f" {m.metrics[key]:>12.2f}"
        output += "\n"
    
    output += "=" * 70 + "\n"
    
    return output
