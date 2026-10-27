#!/usr/bin/env python3
"""
Warehouse layout model. Loads grid configuration from JSON and builds
the directed graph G=(V,A) representing admissible moves between cells.
"""

import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Cell:
    """Represents a single cell in the warehouse grid."""
    
    def __init__(self, row: int, col: int, cell_type: str, name: Optional[str] = None):
        self.row = row
        self.col = col
        self.cell_type = cell_type  # 'lane', 'pickup', 'delivery', 'charge', 'park', 'empty'
        self.name = name or f"{cell_type}_{row}_{col}"
    
    def key(self) -> Tuple[int, int]:
        return (self.row, self.col)
    
    def __repr__(self):
        if self.cell_type == 'lane':
            return '.'
        elif self.cell_type == 'pickup':
            return self.name[-1] if self.name else 'P'
        elif self.cell_type == 'delivery':
            return self.name[-1] if self.name else 'D'
        elif self.cell_type == 'charge':
            return self.name[-1] if self.name else 'C'
        elif self.cell_type == 'park':
            return self.name[-1] if self.name else 'K'
        else:
            return '#'


class Warehouse:
    """Warehouse grid with directed graph of admissible moves."""
    
    def __init__(self, layout_path: str):
        self.layout_path = Path(layout_path)
        self.cells: Dict[Tuple[int, int], Cell] = {}
        self.graph = nx.DiGraph()
        self.rows = 0
        self.cols = 0
        self.load_layout()
    
    def load_layout(self):
        """Load warehouse layout from JSON file."""
        with open(self.layout_path, 'r') as f:
            data = json.load(f)
        
        self.rows = data['dimensions']['rows']
        self.cols = data['dimensions']['cols']
        
        # Initialize all cells as empty
        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(row, col, 'empty')
                self.cells[cell.key()] = cell
                self.graph.add_node(cell.key())
        
        # Add lane cells
        for lane in data['lanes'].get('cells', []):
            row, col = lane['row'], lane['col']
            cell = self.cells.get((row, col))
            if cell:
                cell.cell_type = 'lane'
                self._add_lane_connection(lane)
        
        # Add pickup stations
        for p in data['buffers'].get('pickup_stations', []):
            cell = self.cells[(p['row'], p['col'])]
            cell.cell_type = 'pickup'
            cell.name = p['name']
        
        # Add delivery stations
        for d in data['buffers'].get('delivery_stations', []):
            cell = self.cells[(d['row'], d['col'])]
            cell.cell_type = 'delivery'
            cell.name = d['name']
        
        # Add charging ports
        for c in data['buffers'].get('charging_ports', []):
            cell = self.cells[(c['row'], c['col'])]
            cell.cell_type = 'charge'
            cell.name = c['name']
        
        # Add parking
        for k in data['buffers'].get('parking', []):
            cell = self.cells[(k['row'], k['col'])]
            cell.cell_type = 'park'
            cell.name = k['name']
    
    def _add_lane_connection(self, lane: dict):
        """Add directed edge from lane cell to next cell in direction."""
        row, col = lane['row'], lane['col']
        direction = lane.get('dir', 'east')
        
        if direction == 'east':
            next_cell = (row, col + 1)
        elif direction == 'west':
            next_cell = (row, col - 1)
        elif direction == 'north':
            next_cell = (row - 1, col)
        elif direction == 'south':
            next_cell = (row + 1, col)
        else:
            return
        
        if next_cell in self.graph.nodes:
            self.graph.add_edge((row, col), next_cell)
    
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get cell at position."""
        return self.cells.get((row, col))
    
    def get_route(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Compute shortest path from start to goal using Dijkstra."""
        try:
            return nx.shortest_path(self.graph, start, goal)
        except nx.NetworkXNoPath:
            return []
    
    def distance(self, start: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """Number of moves from start to goal."""
        route = self.get_route(start, goal)
        return len(route) - 1 if route else float('inf')
    
    def render_ascii(self) -> str:
        """Render warehouse as ASCII grid."""
        lines = []
        
        # Header
        header = "     " + "".join([f"{i%10}" for i in range(self.cols)])
        lines.append(header)
        lines.append("    " + "-" * self.cols)
        
        # Grid rows
        for row in range(self.rows):
            line = f" {row} │ "
            for col in range(self.cols):
                cell = self.cells.get((row, col))
                if cell:
                    line += str(cell)
                else:
                    line += '#'
            lines.append(line)
        
        # Legend
        lines.append("")
        lines.append("Legend:")
        lines.append("  . = lane cell, # = empty space")
        lines.append("  P1-5 = pick-up stations, D1-3 = delivery stations")
        lines.append("  C1-4 = charging ports, K1-6 = parking places")
        
        return "\n".join(lines)


def create_warehouse_layout(layout_path: str = "data/layouts/warehouse_15x8.json") -> Warehouse:
    """Factory function to create warehouse instance."""
    return Warehouse(layout_path)


if __name__ == "__main__":
    # Test
    warehouse = create_warehouse_layout()
    print(warehouse.render_ascii())
