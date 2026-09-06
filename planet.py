"""Planet class representing a single planet in the solar system.

Educational note: simple data-holding class with methods is a common
introductory OOP pattern (similar to many university Python tutorials).
"""

from __future__ import annotations


class Planet:
    """A planet with physical properties and a list of major moons.

    Attributes:
        name: Common English name of the planet.
        mass_kg: Approximate mass in kilograms.
        distance_au: Average orbital distance from the Sun in astronomical units.
        moons: Names of major moons (empty for Mercury and Venus).
    """

    def __init__(
        self,
        name: str,
        mass_kg: float,
        distance_au: float,
        moons: list[str] | None = None,
    ) -> None:
        """Create a Planet instance.

        Args:
            name: Planet name (e.g. "Earth").
            mass_kg: Mass in kilograms.
            distance_au: Distance from the Sun in AU.
            moons: Optional list of moon names; defaults to empty list.
        """
        self.name = name
        self.mass_kg = float(mass_kg)
        self.distance_au = float(distance_au)
        # Copy the list so callers cannot mutate our internal state accidentally.
        self.moons: list[str] = list(moons) if moons is not None else []

    def moon_count(self) -> int:
        """Return how many major moons are recorded for this planet."""
        return len(self.moons)

    def describe(self) -> str:
        """Return a multi-line human-readable description of the planet."""
        moon_text = (
            ", ".join(self.moons) if self.moons else "(none listed)"
        )
        return (
            f"Planet: {self.name}\n"
            f"  Mass: {self.mass_kg:.6e} kg\n"
            f"  Distance from Sun: {self.distance_au} AU\n"
            f"  Moons ({self.moon_count()}): {moon_text}"
        )

    def __repr__(self) -> str:
        return (
            f"Planet(name={self.name!r}, mass_kg={self.mass_kg!r}, "
            f"distance_au={self.distance_au!r}, moons={self.moons!r})"
        )

    def __str__(self) -> str:
        return self.describe()
