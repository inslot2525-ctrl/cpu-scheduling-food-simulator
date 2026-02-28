"""
Gantt Chart Visualization for CPU Scheduling Simulation.
Creates visual representations of order scheduling timelines.
"""
from typing import List, Tuple, Dict, Optional
import sys


class GanttChart:
    """
    ASCII-based Gantt chart generator for scheduling visualization.
    """
    
    def __init__(self, title: str = "Scheduling Gantt Chart"):
        self.title = title
        self.colors = {}
        self.order_names = {}
    
    def set_order_names(self, names: Dict[int, str]):
        """Set display names for order IDs."""
        self.order_names = names
    
    def generate(self, gantt_data: List[Tuple[int, int, int]], 
                 max_width: int = 60) -> str:
        """
        Generate ASCII Gantt chart.
        
        Args:
            gantt_data: List of (order_id, start_time, end_time) tuples
            max_width: Maximum character width for the chart
            
        Returns:
            ASCII string representation of the Gantt chart
        """
        if not gantt_data:
            return "No data to display"
        
        # Calculate time range
        min_time = min(start for _, start, _ in gantt_data)
        max_time = max(end for _, _, end in gantt_data)
        time_range = max_time - min_time
        
        if time_range == 0:
            return "No time range to display"
        
        # Calculate scale
        scale = max_width / time_range
        
        # Build chart
        output = []
        output.append("\n" + "═" * (max_width + 20))
        output.append(f"  {self.title}")
        output.append("═" * (max_width + 20))
        
        # Create timeline
        timeline = [' '] * max_width
        
        # Process each segment
        segments_by_order = {}
        for order_id, start, end in gantt_data:
            if order_id not in segments_by_order:
                segments_by_order[order_id] = []
            segments_by_order[order_id].append((start, end))
        
        # Draw each order's timeline
        for order_id in sorted(segments_by_order.keys()):
            segments = segments_by_order[order_id]
            line = [' '] * max_width
            
            for start, end in segments:
                start_pos = int((start - min_time) * scale)
                end_pos = int((end - min_time) * scale)
                start_pos = max(0, min(start_pos, max_width - 1))
                end_pos = max(0, min(end_pos, max_width))
                
                for i in range(start_pos, end_pos):
                    if i < max_width:
                        line[i] = '█'
            
            order_name = self.order_names.get(order_id, f"Order {order_id}")
            output.append(f"  {order_name:<12} │{''.join(line)}│")
        
        # Time axis
        output.append("  " + " " * 12 + "└" + "─" * max_width + "┘")
        
        # Time labels
        time_labels = f"  {' ' * 12}  {min_time:<{max_width//2}}{max_time:>{max_width//2}}"
        output.append(time_labels)
        output.append(f"  {' ' * 12}  {'Time Units':^{max_width}}")
        output.append("═" * (max_width + 20))
        
        return "\n".join(output)
    
    def generate_detailed(self, gantt_data: List[Tuple[int, int, int]]) -> str:
        """
        Generate a detailed text-based timeline.
        
        Args:
            gantt_data: List of (order_id, start_time, end_time) tuples
            
        Returns:
            Detailed timeline string
        """
        if not gantt_data:
            return "No data to display"
        
        output = []
        output.append("\n┌─────────────────────────────────────────────────────────────┐")
        output.append("│                    DETAILED TIMELINE                        │")
        output.append("├──────────┬──────────┬──────────┬───────────────────────────┤")
        output.append("│ Order ID │  Start   │   End    │        Duration           │")
        output.append("├──────────┼──────────┼──────────┼───────────────────────────┤")
        
        for order_id, start, end in gantt_data:
            duration = end - start
            bar = "▓" * min(duration * 2, 20)
            order_name = self.order_names.get(order_id, str(order_id))
            output.append(f"│ {order_name:^8} │ {start:^8} │ {end:^8} │ {bar:<25} │")
        
        output.append("└──────────┴──────────┴──────────┴───────────────────────────┘")
        
        return "\n".join(output)


def create_gantt_chart(gantt_data: List[Tuple[int, int, int]], 
                       title: str = "Gantt Chart",
                       order_names: Optional[Dict[int, str]] = None) -> str:
    """
    Convenience function to create a Gantt chart.
    
    Args:
        gantt_data: List of (order_id, start_time, end_time) tuples
        title: Chart title
        order_names: Optional mapping of order IDs to names
        
    Returns:
        ASCII Gantt chart string
    """
    chart = GanttChart(title)
    if order_names:
        chart.set_order_names(order_names)
    return chart.generate(gantt_data)
