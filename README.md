# MashupGenerator

A command-line tool that scans my music library and recommends acapella/instrumental pairings for mashups and DJ sets, based on musical key compatibility and tempo.

Given an instrumental, it finds every acapella in the library that can be mixed harmonically with it — including tracks that become compatible after a small pitch shift — and tells you exactly how many semitones to shift.

## How it works

The library is indexed into a MariaDB database, then queried with harmonic-mixing rules:

1. **Key matching** — an acapella is considered compatible if it's in the same key as the instrumental or its relative major/minor (e.g. C major ↔ A minor).
2. **Adjacent-key expansion** — optionally widens the search to keys one semitone away, and reports the pitch shift (+1/-1 semitone) needed to bring the acapella into key.
3. **Tempo matching** — tracks are matched if their BPMs are within 15 of each other, including half-time and double-time relationships (a 70 BPM acapella still works over a 140 BPM instrumental).

## Scripts

| Script | Purpose |
|---|---|
| `FindCompatibleSongs.py` | The main CLI — prompts for an instrumental and prints compatible acapellas with tempo and pitch-shift suggestions |
| `DBFiller.py` | Scans the instrumentals folder and populates the database |
| `acapellaDBFiller.py` | Same, for the acapella library |
| `checkScaleFreq.py` | Reports which keys are most common in the library — useful for deciding what to hunt for next |
| `addTypeToDB.py` | One-off migration to tag rows as instrumental vs. acapella |
| `tuneBatSraper.py` | Prototype scraper for pulling key/BPM data from Tunebat |

## Stack

Python · MariaDB (via `mariadb` connector) · BeautifulSoup + pandas (scraper prototype)

## Notes

This was built for my own library, so the loader scripts point at local folder paths and a local database — it's a personal tool rather than a packaged app. The interesting part is the key-compatibility logic in `FindCompatibleSongs.py`: relative-scale lookup, adjacent-key expansion, and tempo matching with half/double-time handling.
