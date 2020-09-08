# bike-graphics

Tools for loading GPX files, and analysing/graphing.

First step: convert GPX files to CSV:

```
$ gpx2csv.py MyRoute.gpx > MyRoute.csv
```

Multiple gpx files can be listed in the above command.

Get the summary data using stats.py:

```
$ stats.py MyRoute.csv
Distance: 156.66km
Moving Time: 06:52:20
Total Time: 0 days 08:03:40
Average Speed: 22.80km/h
Max Speed: 69.07km/h
Ascent: 1979m
Descent: -1716m
```

Currently this differs slightly from the Strava stats for the same ride, which are:

```
Distance: 157.29km
Moving Time: 06:54:19
Total Time: 08:03:40
Average Speed: 22.8km/h
Max Speed: 67.0km/h
Ascent: 2106m
Descent: NA
```

## Plotting Data

Data can be plotted with gnuplot - there's a gpx.gp file to load in that defines some of the column indices and sets up gnuplot for the csv format:

```
gnuplot> load 'gpx.gp'
gnuplot> plot 'MyRoute.csv' u c_elapsed:c_elev w l
```

`plot.py` uses matplotlib to produce results, currently only for a single column:

```
$ plot.py MyRoute.csv alt --smooth 50
```

## Plotting on a Map (Folium)

```
$ fol.py MyRoute.csv -o test.html
$ xdg-open test.html
```


## Plotting on a Map (Matplotlib)

Work out the tiles required:

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
