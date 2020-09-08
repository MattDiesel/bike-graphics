
import pandas as pd
import numpy as np
import folium
import sys

import argparse

parser = argparse.ArgumentParser(description='Create a graph')

parser.add_argument('file', help='CSV file to use')
parser.add_argument('-o', '--output', help='Output HTML file.')
parser.add_argument('-z', '--zoom', type=int, default=11, help='Zoom level (default 11)')

args = parser.parse_args()

df = pd.read_csv(args.file, index_col='time', parse_dates=True)


latMin = min(df['lat'])
lonMin = min(df['lon'])
latMax = max(df['lat'])
lonMax = max(df['lon'])


m = folium.Map(location=[(latMax+latMin)*0.5, (lonMax+lonMin)*0.5],
              zoom_start=args.zoom, tiles='Stamen Terrain')

n = 100
p = list(zip(df['lat'].to_numpy()[::n], df['lon'].to_numpy()[::n]))

folium.PolyLine(p, color="red", weight=5, opacity=1).add_to(m)

if not args.output:
    print("Output file required")
else:
    m.save(args.output)



