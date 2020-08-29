
import pandas as pd
import argparse
import sys
from gpxanalysis import *

parser = argparse.ArgumentParser(description='Create an image of a track overlayed on a map')

parser.add_argument('files', help='GPX file to use', nargs='+')
parser.add_argument('-o', '--output', help='Output csv file.')

args = parser.parse_args()


df = pd.concat([pd.read_csv(f, index_col='time', parse_dates=True) for f in args.files], axis=0)

df.sort_index(inplace=True)
df = gpxAnalyse(df)


if not args.output:
    df.to_csv(sys.stdout)
else:
    df.to_csv(args.output)
