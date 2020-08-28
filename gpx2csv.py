import gpxpy
import pandas as pd
import argparse
import sys


def gpxGetPoints(gpx):
	return gpx.tracks[0].segments[0].points


def gpxPointsToDataframe(points):
	df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
	for point in points:
		df = df.append({'time' : point.time, 'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation}, ignore_index=True)

	return df

def gpxLoadFile(f):
	with open(f, 'r') as gpx_file:
		gpx = gpxpy.parse(gpx_file)

	return gpx


def dfLoadGPX(f):
	gpx = gpxLoadFile(f)
	points = gpxGetPoints(gpx)
	return gpxPointsToDataframe(points)


parser = argparse.ArgumentParser(description='Create an image of a track overlayed on a map')

parser.add_argument('file', help='GPX file to use')
parser.add_argument('-o', '--output', help='Output csv file.')

args = parser.parse_args()

df = dfLoadGPX(args.file)

if not args.output:
	df.to_csv(sys.stdout, index=False)
else:
	df.to_csv(args.output, index=False)





