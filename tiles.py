
import gpxpy
import math
import argparse
import pandas as pd


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


parser = argparse.ArgumentParser(description='Calculate required tiles for a zoom level')

parser.add_argument('file', help='CSV file to use')
parser.add_argument('--zoom', type=int, default=11, help='Zoom level (default 11)')

parser.add_argument('-c', '--coords', action="store_true")
parser.add_argument('-t', '--tiles', action="store_true")
parser.add_argument('-e', '--extents', action="store_true")
parser.add_argument('-n', '--tilecount', action="store_true")
parser.add_argument('-p', '--pixels', action="store_true")
parser.add_argument('-s', '--command', action="store_true")


args = parser.parse_args()

df = pd.read_csv(args.file, index_col='time', parse_dates=True)

latMin = min(df['lat'])
latMax = max(df['lat'])
lonMin = min(df['lon'])
lonMax = max(df['lon'])

xmin, ymax = deg2num(latMin, lonMin, args.zoom)
xmax, ymin = deg2num(latMax, lonMax, args.zoom)

extR, extT = num2deg(xmin,ymin,args.zoom)
extL, extB = num2deg(xmax+1,ymax+1,args.zoom)



cmds = """curl http://a.tile.openstreetmap.org/{0}/[{1}-{2}]/[{3}-{4}].png -o "tiles/{0}/#1/#2.png" --create-dirs"""

if args.coords:
    print("({0:.5f},{1:.5f}) - ({2:.5f},{3:.5f})".format(latMin, lonMin, latMax, lonMax))

if args.tiles:
    print("({0},{1}) - ({2},{3})".format(xmin,ymin,xmax,ymax))

if args.extents:
    print("({0:.5f},{1:.5f}) - ({2:.5f},{3:.5f})".format(extL, extT, extR, extB))

if args.tilecount:
    print("{0}".format((xmax-xmin+1)*(ymax-ymin+1)))

if args.pixels:
    print("{0}x{1}".format((xmax-xmin+1)*256, (ymax-ymin+1)*256))

if args.command:
    print("{0}".format(cmds.format(args.zoom, xmin, xmax, ymin, ymax)))

if True not in [args.coords, args.tiles, args.extents, args.tilecount, args.pixels, args.command]:
    print("Zoom level: {0}".format(args.zoom))
    print("Coordinates: ({0:.5f},{1:.5f}) - ({2:.5f},{3:.5f})".format(latMin, lonMin, latMax, lonMax))
    print("Tiles: ({0},{1}) - ({2},{3})".format(xmin,ymin,xmax,ymax))
    print("Tile Extents: ({0:.5f},{1:.5f}) - ({2:.5f},{3:.5f})".format(extL, extT, extR, extB))

    print("Number of tiles: {0}".format((xmax-xmin+1)*(ymax-ymin+1)))

    print("Pixels: {0}x{1}".format((xmax-xmin+1)*256, (ymax-ymin+1)*256))

    print("Run: {0}".format(cmds.format(args.zoom, xmin, xmax, ymin, ymax)))






