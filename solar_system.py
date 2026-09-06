"""SolarSystem class: load planets from JSON and answer lookups.

Educational note: loading domain objects from a JSON file and providing
case-insensitive lookup by name is a common pattern in introductory
Python projects (file I/O + dictionaries + OOP).
"""

from __future__ import annotations

import json
from pathlib import Path

from planet import Planet


class PlanetNotFoundError(LookupError):
    """Raised when a requested planet name is not in the solar system data."""


class SolarSystem:
    """Collection of planets loaded from a JSON data file.

    Provides case-insensitive lookup and helper methods used by the
    interactive menu and by unit tests.
    """

    def __init__(self, data_path: str | Path) -> None:
        """Load planets from the given JSON file path.

        Args:
            data_path: Path to planets.json (absolute or relative).

        Raises:
            FileNotFoundError: If the JSON file does not exist.
            ValueError: If the JSON structure is invalid.
        """
        self._data_path = Path(data_path)
        self._planets: dict[str, Planet] = {}
        self._meta: dict = {}
        self._load()

    def _load(self) -> None:
        """Read JSON and build Planet objects keyed by lowercase name."""
        with self._data_path.open(encoding="utf-8") as fh:
            payload = json.load(fh)

        if not isinstance(payload, dict) or "planets" not in payload:
            raise ValueError("JSON must contain a top-level 'planets' list")

        self._meta = payload.get("_meta", {})
        planets_raw = payload["planets"]
        if not isinstance(planets_raw, list):
            raise ValueError("'planets' must be a list")

        for entry in planets_raw:
            planet = Planet(
                name=entry["name"],
                mass_kg=entry["mass_kg"],
                distance_au=entry["distance_au"],
                moons=entry.get("moons", []),
            )
            key = planet.name.casefold()
            self._planets[key] = planet

    @property
    def meta(self) -> dict:
        """Return metadata from the JSON file (e.g. data source citation)."""
        return dict(self._meta)

    def list_planets(self) -> list[str]:
        """Return planet names in the order they were loaded from the file."""
        # Preserve insertion order (Python 3.7+ dict order).
        return [p.name for p in self._planets.values()]

    def is_planet(self, name: str) -> bool:
        """Return True if name matches a loaded planet (case-insensitive)."""
        return name.strip().casefold() in self._planets

    def get_planet(self, name: str) -> Planet:
        """Return the Planet object for the given name.

        Args:
            name: Planet name (case-insensitive; surrounding spaces ignored).

        Raises:
            PlanetNotFoundError: If the name is not in the data set.
        """
        key = name.strip().casefold()
        if key not in self._planets:
            raise PlanetNotFoundError(f"Unknown planet: {name!r}")
        return self._planets[key]

    def get_mass(self, name: str) -> float:
        """Return mass in kilograms for the named planet."""
        return self.get_planet(name).mass_kg

    def get_moons(self, name: str) -> list[str]:
        """Return a copy of the moon name list for the named planet."""
        return list(self.get_planet(name).moons)

    def get_details(self, name: str) -> str:
        """Return the full describe() text for the named planet."""
        return self.get_planet(name).describe()

    def __len__(self) -> int:
        return len(self._planets)

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, str):
            return False
        return self.is_planet(name)
