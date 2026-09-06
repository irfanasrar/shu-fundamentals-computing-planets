"""Interactive PlanetApp menu for the solar system program.

Educational note: a simple text menu loop with input validation is a
standard console-app pattern taught in many Fundamentals of Computing
courses (menu options + while True + try/except around lookups).
"""

from __future__ import annotations

from solar_system import PlanetNotFoundError, SolarSystem


class PlanetApp:
    """Command-line menu that queries a SolarSystem instance."""

    MENU_TEXT = """
========================================
  Solar System Planets Explorer
========================================
  1. List all planets
  2. Full details about a planet
  3. Mass of a planet
  4. Is a name in the planet list?
  5. How many moons does a planet have?
  6. List moons of a planet
  0. Quit
========================================
"""

    def __init__(self, solar_system: SolarSystem) -> None:
        """Attach this app to an already-loaded SolarSystem."""
        self.system = solar_system

    def run(self) -> None:
        """Run the interactive menu until the user quits."""
        print("Welcome to the Solar System Planets program.")
        source = self.system.meta.get("source", "")
        if source:
            print(f"Data note: {source}")
        print()

        while True:
            print(self.MENU_TEXT)
            choice = input("Enter option number: ").strip()

            if choice == "":
                print("Error: empty input. Please enter a menu number.\n")
                continue

            if choice == "0":
                print("Goodbye!")
                break
            if choice == "1":
                self._list_planets()
            elif choice == "2":
                self._full_details()
            elif choice == "3":
                self._mass()
            elif choice == "4":
                self._is_planet()
            elif choice == "5":
                self._moon_count()
            elif choice == "6":
                self._list_moons()
            else:
                print(
                    f"Error: unknown menu option {choice!r}. "
                    "Please choose 0–6.\n"
                )

    def _ask_planet_name(self) -> str | None:
        """Prompt for a planet name; return None if the user left it empty."""
        name = input("Enter planet name: ").strip()
        if name == "":
            print("Error: planet name cannot be empty.\n")
            return None
        return name

    def _list_planets(self) -> None:
        names = self.system.list_planets()
        print(f"\nPlanets in this data set ({len(names)}):")
        for i, name in enumerate(names, start=1):
            print(f"  {i}. {name}")
        print()

    def _full_details(self) -> None:
        name = self._ask_planet_name()
        if name is None:
            return
        try:
            print()
            print(self.system.get_details(name))
            print()
        except PlanetNotFoundError:
            print(
                f"Error: '{name}' is not a known planet in this list. "
                "Try option 1 to see valid names.\n"
            )

    def _mass(self) -> None:
        name = self._ask_planet_name()
        if name is None:
            return
        try:
            mass = self.system.get_mass(name)
            print(f"\nMass of {self.system.get_planet(name).name}: {mass:.6e} kg\n")
        except PlanetNotFoundError:
            print(
                f"Error: '{name}' is not a known planet in this list. "
                "Try option 1 to see valid names.\n"
            )

    def _is_planet(self) -> None:
        name = self._ask_planet_name()
        if name is None:
            return
        if self.system.is_planet(name):
            print(f"\nYes — '{name}' is a planet in this list.\n")
        else:
            print(f"\nNo — '{name}' is NOT a planet in this list.\n")

    def _moon_count(self) -> None:
        name = self._ask_planet_name()
        if name is None:
            return
        try:
            planet = self.system.get_planet(name)
            count = planet.moon_count()
            print(f"\n{planet.name} has {count} major moon(s) listed.\n")
        except PlanetNotFoundError:
            print(
                f"Error: '{name}' is not a known planet in this list. "
                "Try option 1 to see valid names.\n"
            )

    def _list_moons(self) -> None:
        name = self._ask_planet_name()
        if name is None:
            return
        try:
            planet = self.system.get_planet(name)
            moons = planet.moons
            if moons:
                print(f"\nMajor moons of {planet.name}:")
                for m in moons:
                    print(f"  - {m}")
                print()
            else:
                print(f"\n{planet.name} has no moons listed in this data set.\n")
        except PlanetNotFoundError:
            print(
                f"Error: '{name}' is not a known planet in this list. "
                "Try option 1 to see valid names.\n"
            )
