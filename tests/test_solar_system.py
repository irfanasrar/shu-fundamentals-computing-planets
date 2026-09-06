"""Unit tests for SolarSystem / Planet (stdlib unittest only).

Run from the project root:
    python -m unittest
    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure project root is on sys.path when running tests as a package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from planet import Planet  # noqa: E402
from solar_system import PlanetNotFoundError, SolarSystem  # noqa: E402

DATA_PATH = PROJECT_ROOT / "data" / "planets.json"


class TestPlanet(unittest.TestCase):
    """Basic Planet object behaviour."""

    def test_moon_count_and_describe(self) -> None:
        earth = Planet("Earth", 5.97237e24, 1.0, ["Moon"])
        self.assertEqual(earth.moon_count(), 1)
        text = earth.describe()
        self.assertIn("Earth", text)
        self.assertIn("Moon", text)

    def test_empty_moons_default(self) -> None:
        mercury = Planet("Mercury", 3.3011e23, 0.387)
        self.assertEqual(mercury.moon_count(), 0)
        self.assertEqual(mercury.moons, [])


class TestSolarSystem(unittest.TestCase):
    """Tests that load the real planets.json data file."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.system = SolarSystem(DATA_PATH)

    def test_loads_eight_planets(self) -> None:
        self.assertEqual(len(self.system), 8)
        names = self.system.list_planets()
        self.assertEqual(
            names,
            [
                "Mercury",
                "Venus",
                "Earth",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune",
            ],
        )

    def test_case_insensitive_lookup(self) -> None:
        self.assertTrue(self.system.is_planet("saturn"))
        self.assertTrue(self.system.is_planet("SATURN"))
        self.assertTrue(self.system.is_planet("  Saturn  "))
        planet = self.system.get_planet("saTuRn")
        self.assertEqual(planet.name, "Saturn")

    def test_pluto_is_not_a_planet_in_list(self) -> None:
        """Brief example: Is Pluto a planet in the list? -> No."""
        self.assertFalse(self.system.is_planet("Pluto"))
        self.assertFalse(self.system.is_planet("pluto"))
        self.assertNotIn("Pluto", self.system.list_planets())

    def test_earth_moon_count(self) -> None:
        """Brief example: How many moons does Earth have? -> 1 (Moon)."""
        earth = self.system.get_planet("Earth")
        self.assertEqual(earth.moon_count(), 1)
        self.assertEqual(self.system.get_moons("Earth"), ["Moon"])

    def test_mass_of_neptune(self) -> None:
        """Brief example: Mass of Neptune."""
        mass = self.system.get_mass("Neptune")
        self.assertIsInstance(mass, float)
        # Rough Wikipedia-scale check (order of magnitude ~1e26 kg).
        self.assertGreater(mass, 1.0e25)
        self.assertLess(mass, 2.0e26)
        self.assertAlmostEqual(mass, 1.02413e26, places=0)

    def test_saturn_full_details(self) -> None:
        """Brief example: Everything about Saturn."""
        details = self.system.get_details("Saturn")
        self.assertIn("Saturn", details)
        self.assertIn("Titan", details)
        moons = self.system.get_moons("Saturn")
        self.assertIn("Titan", moons)
        self.assertIn("Enceladus", moons)
        self.assertGreaterEqual(len(moons), 4)

    def test_jupiter_galilean_moons(self) -> None:
        moons = self.system.get_moons("Jupiter")
        for expected in ("Io", "Europa", "Ganymede", "Callisto"):
            self.assertIn(expected, moons)

    def test_unknown_planet_raises(self) -> None:
        with self.assertRaises(PlanetNotFoundError):
            self.system.get_planet("Xylophone")
        with self.assertRaises(PlanetNotFoundError):
            self.system.get_mass("Pluto")

    def test_contains_protocol(self) -> None:
        self.assertIn("Earth", self.system)
        self.assertNotIn("Pluto", self.system)

    def test_meta_cites_wikipedia(self) -> None:
        meta = self.system.meta
        self.assertIn("source", meta)
        self.assertIn("Wikipedia", meta["source"])


if __name__ == "__main__":
    unittest.main()
