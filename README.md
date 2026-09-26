# Our Travel Map

An interactive world map of everywhere we've been. Visited countries are shaded,
cities get a pin, and clicking any of them opens a panel with the Wikipedia summary
and our own notes.

## Files

| File | What it is |
|---|---|
| `index.html` | The map. Open it in a browser. |
| `places.js` | **Our list of places.** The only file you normally edit. |
| `geocode.py` | Helper that looks up and saves coordinates for new cities. |

## How to run it

Double-click `index.html`. It opens in your browser. That's it: no server, no install.
(It needs an internet connection for the map, borders and Wikipedia.)

## How to add a place

1. Open `places.js` in any text editor (TextEdit works; use *Format → Make Plain Text*).
2. Add a line anywhere between the first and last lines:

   ```
   Barcelona, Spain | 2022 | Sagrada Família finally finished?
   Norway | 2019 | Fjord cruise
   ```

   - **City, Country** adds a pin and shades the country.
   - **Country** on its own just shades the country.
   - After the name, separated by `|`, you can add any of these, in any order:
     - years: `2019`, `2019, 2023`, or `2015-2017`
     - notes: any text
3. Save and refresh the page. New cities are looked up automatically and appear within a
   few seconds. A green note at the top-left lists which ones were looked up.
4. To save those coordinates into the file (so they're never looked up again), open Terminal
   in this folder and run:

   ```bash
   python3 geocode.py
   ```

   It prints where each place was found so you can check it. `python3 geocode.py --dry-run`
   shows the same thing without changing the file.

**Two rules:** don't use the backtick character (`` ` ``) anywhere in `places.js`, and
don't change its first and last lines. If you break either rule, the page and the
helper will both tell you.

Country names are flexible: `USA`, `UK`, `Scotland`, `Holland`, `Czech Republic`,
`The Netherlands` and so on all work. If a name isn't recognised, a yellow note on
the map tells you which line to fix.

## How to fix a place that's in the wrong spot

Every city line ends with its coordinates, like `| 48.4283, -123.3650`.

1. Find the right spot on [openstreetmap.org](https://www.openstreetmap.org), right-click it
   and choose **Show address**. The coordinates appear on the left. (Or in Google Maps,
   right-click and click the numbers at the top of the menu to copy them.)
2. Replace the coordinates at the end of that line in `places.js` and save.

Coordinates you type are never overwritten. The helper only fills in lines that have none.

You can also avoid the problem up front by being more specific:
`Victoria, Canada` → `Victoria, British Columbia, Canada`.

**Wrong Wikipedia article?** Add `wiki: Exact Page Title` to the line, using the title
from the Wikipedia page's address, for example:

```
Paris, United States | 2016 | wiki: Paris, Texas
```

## Where things come from

Everything loads at runtime from these free services. Nothing is installed.

| What | Source | Terms |
|---|---|---|
| Map library | [Leaflet](https://leafletjs.com) 1.9.4 via cdnjs, pinned to that version with integrity checks | Open source (BSD) |
| Map background | [OpenStreetMap](https://www.openstreetmap.org) standard tiles, greyed with CSS | Free for light use under the [tile usage policy](https://operations.osmfoundation.org/policies/tiles/); credit shown bottom-right |
| Country borders | [Natural Earth](https://www.naturalearthdata.com) 1:50m countries, v5.1.2, via jsDelivr | Public domain |
| Coordinates | [Nominatim](https://nominatim.org) (OpenStreetMap) | Max 1 request per second, no bulk use, results must be cached ([policy](https://operations.osmfoundation.org/policies/nominatim/)). Saving to `places.js` is that cache. |
| Summaries and photos | [Wikipedia](https://en.wikipedia.org) and [Wikidata](https://www.wikidata.org) APIs | Free; text is CC BY-SA, which the "Read more on Wikipedia" link credits |
