#!/usr/bin/env python3
"""
ASCII visualization of warehouse state.
Runs without ROS - pure Python.
"""

import sys
sys.path.insert(0, '.')

from src.model.warehouse import create_warehouse_layout


def main():
    warehouse = create_warehouse_layout()
    print(warehouse.render_ascii())


if __name__ == "__main__":
    main()
