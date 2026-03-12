"""
Dashboard for displaying scheduling simulation results.
Combines Gantt charts, metrics, and order details in a unified view.
"""
from typing import List, Dict, Tuple, Optional
from scheduler_engine.order import Order
from metrics.performance import PerformanceMetrics
from .gantt_chart import GanttChart


class Dashboard:
    """
    Unified dashboard for scheduling simulation visualization.
    """
    
    def __init__(self, title: str = "CPU Scheduling Food Simulator"):
        self.title = title
    
    def display(self, 
                orders: List[Order], 
                gantt_data: List[Tuple[int, int, int]], 
                algorithm_name: str) -> str:
        """
        Display a complete dashboard for a single algorithm run.
        
        Args:
            orders: List of completed orders
            gantt_data: Gantt chart data
            algorithm_name: Name of the scheduling algorithm
            
        Returns:
            Formatted dashboard string
        """
        output = []
        
        # Header
        output.append("\n" + "╔" + "═" * 68 + "╗")
        output.append(f"║{self.title:^68}║")
        output.append("╠" + "═" * 68 + "╣")
        output.append(f"║  Algorithm: {algorithm_name:<54}║")
        output.append("╚" + "═" * 68 + "╝")
        
        # Order details table
        output.append(self._generate_order_table(orders))
        
        # Gantt chart
        order_names = {o.order_id: o.name[:10] for o in orders}
        chart = GanttChart(f"{algorithm_name} Schedule")
        chart.set_order_names(order_names)
        output.append(chart.generate(gantt_data))
        output.append(chart.generate_detailed(gantt_data))
        
        # Performance metrics
        metrics = PerformanceMetrics(orders, algorithm_name)
        output.append(metrics.get_summary())
        
        return "\n".join(output)
    
    def _generate_order_table(self, orders: List[Order]) -> str:
        """Generate a formatted table of order details."""
        output = []
        output.append("\n┌────────────────────────────────────────────────────────────────────┐")
        output.append("│                           ORDER DETAILS                            │")
        output.append("├─────┬────────────┬─────────┬──────────┬──────────┬─────────┬───────┤")
        output.append("│ ID  │    Name    │ Arrival │ Prep Time│ Priority │ Wait    │ TAT   │")
        output.append("├─────┼────────────┼─────────┼──────────┼──────────┼─────────┼───────┤")
        
        for order in sorted(orders, key=lambda x: x.order_id):
            wait = order.waiting_time if order.waiting_time is not None else "-"
            tat = order.turnaround_time if order.turnaround_time is not None else "-"
            output.append(
                f"│ {order.order_id:>3} │ {order.name[:10]:<10} │ {order.arrival_time:>7} │ "
                f"{order.preparation_time:>8} │ {order.priority:>8} │ {str(wait):>7} │ {str(tat):>5} │"
            )
        
        output.append("└─────┴────────────┴─────────┴──────────┴──────────┴─────────┴───────┘")
        return "\n".join(output)
    
    def compare_algorithms(self, 
                           results: Dict[str, Tuple[List[Order], List[Tuple[int, int, int]]]]) -> str:
        """
        Display comparison dashboard for multiple algorithms.
        
        Args:
            results: Dictionary mapping algorithm names to (orders, gantt_data) tuples
            
        Returns:
            Formatted comparison dashboard string
        """
        output = []
        
        # Header
        output.append("\n" + "╔" + "═" * 68 + "╗")
        output.append(f"║{'ALGORITHM COMPARISON DASHBOARD':^68}║")
        output.append("╚" + "═" * 68 + "╝")
        
        # Generate individual Gantt charts
        for name, (orders, gantt_data) in results.items():
            order_names = {o.order_id: o.name[:8] for o in orders}
            chart = GanttChart(name)
            chart.set_order_names(order_names)
            output.append(chart.generate(gantt_data, max_width=50))
        
        # Comparison table
        output.append("\n" + "═" * 70)
        output.append("METRICS COMPARISON")
        output.append("═" * 70)
        
        metrics_list = {}
        for name, (orders, _) in results.items():
            metrics_list[name] = PerformanceMetrics(orders, name)
        
        # Header row
        header = f"{'Metric':<25}"
        for name in metrics_list.keys():
            header += f" {name[:12]:>12}"
        output.append(header)
        output.append("─" * 70)
        
        # Metric rows
        metric_keys = [
            ('Avg Waiting Time', 'avg_waiting_time'),
            ('Avg Turnaround Time', 'avg_turnaround_time'),
            ('Avg Response Time', 'avg_response_time'),
            ('Throughput', 'throughput'),
            ('CPU Utilization %', 'cpu_utilization')
        ]
        
        for label, key in metric_keys:
            row = f"{label:<25}"
            for name, metrics in metrics_list.items():
                row += f" {metrics.metrics[key]:>12.2f}"
            output.append(row)
        
        output.append("═" * 70)
        
        # Determine best algorithm for each metric
        output.append("\nBEST PERFORMERS:")
        output.append("─" * 40)
        
        for label, key in metric_keys:
            values = {name: m.metrics[key] for name, m in metrics_list.items()}
            if 'Throughput' in label or 'Utilization' in label:
                best = max(values, key=values.get)
            else:
                best = min(values, key=values.get)
            output.append(f"  {label}: {best}")
        
        return "\n".join(output)


def show_dashboard(orders: List[Order], 
                   gantt_data: List[Tuple[int, int, int]], 
                   algorithm_name: str) -> str:
    """Convenience function to display dashboard."""
    dashboard = Dashboard()
    return dashboard.display(orders, gantt_data, algorithm_name)
