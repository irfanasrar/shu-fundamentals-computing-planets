#!/usr/bin/env python3
"""Entry point for the SHU Fundamentals of Computing solar system program.

Run from the project root:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

from planet_app import PlanetApp
from solar_system import SolarSystem


def default_data_path() -> Path:
    """Return path to data/planets.json next to this script."""
    return Path(__file__).resolve().parent / "data" / "planets.json"


def main() -> None:
    """Load the solar system data and start the interactive menu."""
    data_path = default_data_path()
    if not data_path.is_file():
        raise SystemExit(f"Data file not found: {data_path}")

    system = SolarSystem(data_path)
    app = PlanetApp(system)
    app.run()


if __name__ == "__main__":
    main()
