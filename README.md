# Solar System Planets Program

SHU **Fundamentals of Computing** referral project: an object-oriented Python
console application that stores planet data in JSON and answers interactive
queries (details, mass, moons, membership).

> **Academic integrity:** Understand every line before you submit. Do not
> submit code you cannot explain in a viva or code review. Adapt names and
> comments if your tutor expects your own wording, and be ready to walk
> through `Planet`, `SolarSystem`, and `PlanetApp`.

## Requirements

- Python **3.10+**
- Standard library only (no `pip install`, no web, no database)

## Project structure

```
solar-system-planets/
├── main.py                 # Entry point — run the menu
├── planet.py               # Planet class
├── solar_system.py         # SolarSystem class (JSON load + lookups)
├── planet_app.py           # PlanetApp interactive menu + validation
├── data/
│   └── planets.json        # Mercury–Neptune (Pluto omitted on purpose)
├── tests/
│   ├── __init__.py
│   └── test_solar_system.py
├── TEST_PLAN.md            # Manual test plan
└── README.md               # This file
```

## How to run

From the project root (`solar-system-planets/`):

```bash
python main.py
```

or:

```bash
python3 main.py
```

### Menu options (map to the brief's example queries)

| Option | Action | Example |
|--------|--------|---------|
| 1 | List all planets | — |
| 2 | Full details about a planet | Everything about Saturn |
| 3 | Mass of a planet | Mass of Neptune |
| 4 | Is a name in the list? | Is Pluto a planet in the list? → **No** |
| 5 | Moon count | How many moons does Earth have? → **1** |
| 6 | List moon names | Saturn → Titan, Rhea, … |
| 0 | Quit | — |

Input is validated for empty strings, unknown menu numbers, and unknown
planet names (clear error messages). Planet names are **case-insensitive**.

## Automated tests

```bash
python -m unittest
```

Verbose:

```bash
python -m unittest discover -s tests -v
```

## Data source

Approximate masses, AU distances, and major moon names are taken from
**Wikipedia** (planet and moon articles). See `_meta` inside
`data/planets.json`. Pluto is **not** included so membership queries return
false under the IAU 2006 eight-planet model used by this brief.

## Push to GitHub (student steps)

1. Create a new empty repository on GitHub (do not add a README there if you
   already have this one).
2. In a terminal, from the folder that contains these files:

```bash
cd solar-system-planets
git init
git add .
git commit -m "Initial solar system planets referral project"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Replace `<your-username>` and `<your-repo>` with your own values. Follow any
additional submission instructions from your SHU module (e.g. Blackboard link
to the repo, ZIP upload).

## Design overview

- **`Planet`** — holds name, mass, distance, moons; `describe()`, `moon_count()`.
- **`SolarSystem`** — loads JSON, case-insensitive lookup, `is_planet`,
  `get_mass`, `get_moons`, `get_details`, `list_planets`.
- **`PlanetApp`** — menu loop and validation; depends only on `SolarSystem`.

This separation keeps data, domain logic, and UI in separate classes (clean
OOP for the referral marking criteria).
