# Manual Test Plan — Solar System Planets Program

Run the app with `python main.py` from the project root. Record Pass/Fail
for each case. Automated coverage is in `tests/test_solar_system.py`; this
document focuses on interactive behaviour and edge cases.

## 1. Normal / happy-path queries (brief examples)

| ID | Steps | Expected result |
|----|--------|-----------------|
| N1 | Option **2**, enter `Saturn` | Full details: name Saturn, mass ~5.68e26 kg, distance ~9.537 AU, moons include Titan, Rhea, Enceladus, Mimas (and others listed). |
| N2 | Option **3**, enter `Neptune` | Mass of Neptune printed in scientific notation (~1.024e26 kg). |
| N3 | Option **4**, enter `Pluto` | **No** — Pluto is NOT a planet in this list. |
| N4 | Option **5**, enter `Earth` | Earth has **1** major moon listed. |
| N5 | Option **1** | Lists exactly 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune (in that order). |
| N6 | Option **6**, enter `Jupiter` | Lists Io, Europa, Ganymede, Callisto. |
| N7 | Option **0** | Prints goodbye and exits cleanly. |

## 2. Case-insensitivity and whitespace

| ID | Steps | Expected result |
|----|--------|-----------------|
| C1 | Option 2, enter `saturn` | Same details as Saturn (canonical capitalisation in output). |
| C2 | Option 2, enter `SATURN` | Same as N1. |
| C3 | Option 2, enter `  Earth  ` (spaces) | Earth details shown (name trimmed). |
| C4 | Option 4, enter `pluto` | No — not in list. |

## 3. Invalid / error handling

| ID | Steps | Expected result |
|----|--------|-----------------|
| E1 | At menu, press Enter only (empty) | Clear error: empty input; menu shown again. |
| E2 | Enter menu option `9` | Error: unknown menu option; prompt again. |
| E3 | Enter menu option `abc` | Error: unknown menu option; prompt again. |
| E4 | Option 2, planet name empty (Enter) | Error: planet name cannot be empty. |
| E5 | Option 2, enter `Xylophone` | Error: unknown planet; suggest option 1. |
| E6 | Option 3, enter `Pluto` | Error: not a known planet (mass lookup fails for missing names). |
| E7 | Option 5, enter `Foo` | Error: unknown planet. |

## 4. Boundary / special cases

| ID | Steps | Expected result |
|----|--------|-----------------|
| B1 | Option 5, enter `Mercury` | **0** moons listed. |
| B2 | Option 5, enter `Venus` | **0** moons listed. |
| B3 | Option 6, enter `Mercury` | Message that no moons are listed. |
| B4 | Option 4, enter `Earth` | Yes — Earth is in the list. |
| B5 | Option 4, enter `  ` (spaces only) | Treated as empty name → error. |
| B6 | After an error, choose a valid option | App continues; no crash. |
| B7 | Option 3, enter `mars` | Mass ~6.417e23 kg printed. |

## 5. Smoke checklist after code changes

1. `python -m unittest` → all tests OK.
2. Manually run N1–N4 and E1–E2 once.
3. Confirm `data/planets.json` still has `_meta` citing Wikipedia and **no** Pluto entry.

## 6. Mapping to referral brief queries

| Brief-style question | Menu path | Expected |
|----------------------|-----------|----------|
| Everything about Saturn | 2 → Saturn | Full describe() text |
| Mass of Neptune | 3 → Neptune | Scientific mass |
| Is Pluto a planet in the list? | 4 → Pluto | No |
| How many moons does Earth have? | 5 → Earth | 1 |
