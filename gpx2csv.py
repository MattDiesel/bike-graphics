import gpxpy
import pandas as pd
import argparse
import sys
import datetime
from gpxanalysis import *


parser = argparse.ArgumentParser(description='Convert a GPX file to CSV')

parser.add_argument('files', help='GPX file to use', nargs='+')
parser.add_argument('-o', '--output', help='Output csv file.')

args = parser.parse_args()


dfs = []
for f in args.files:
    with open(f, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    points = gpx.tracks[0].segments[0].points

    df = pd.DataFrame.from_records(({'time' : pd.to_datetime(x.time), 'lon': x.longitude, 'lat' : x.latitude, 'alt' : x.elevation} for x in points), columns=['time', 'lon', 'lat', 'alt'], index='time')

    dfs.append(df)

df = pd.concat(dfs, axis=0)
df.sort_index(inplace=True)
df = gpxAnalyse(df)

if not args.output:
    df.to_csv(sys.stdout)
else:
    df.to_csv(args.output)





