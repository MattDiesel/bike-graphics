# bike-graphics

Tools for loading GPX files, and analysing/graphing.

First step: convert GPX files to CSV:

```
$ gpx2csv.py MyRoute.gpx > MyRoute.csv
```

Can then merge multiple CSV files together using `csvmerge.py`. 

Next, work out the tiles required:

```
$ tiles.py MyRoute.csv
Zoom level: 11
Coordinates: (51.86144,-3.74987) - (52.19328,-2.09383)
Tiles: (1002,674) - (1012,677)
Tile Extents: (51.83578,-3.86719) - (52.26816,-1.93359)
Number of tiles: 44
Pixels: 2816x1024
Run: curl http://a.tile.openstreetmap.org/[11]/[1002-1012]/[674-677].png -o "tiles/#1/#2/#3.png" --create-dirs
```

Can change the zoom level from default of 11 using `--zoom N`. Check the pixels output to make sure it's not going to be crazy big. 

Download required tiles (`-s` prints the just the command from above) :

```
$ tiles.py MyRoute.csv -s | sh
```

Can then generate a basic overlay:

```
$ overlay.py MyRoute.csv
```
