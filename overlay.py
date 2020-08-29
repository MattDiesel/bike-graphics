import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import math
from PIL import Image

import argparse


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

def drawImageCluster(latMin, lonMin, latMax, lonMax, zoom):
	xmin, ymax = deg2num(latMin, lonMin, zoom)
	xmax, ymin = deg2num(latMax, lonMax, zoom)

	a = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
	for xtile in range(xmin, xmax+1):
		for ytile in range(ymin,  ymax+1):
			tf = "tiles/{0}/{1}/{2}.png".format(zoom,xtile,ytile)
			try:
				tile = Image.open(tf)
				a.paste(tile, box=((xtile-xmin)*256 ,  (ytile-ymin)*256))
			except: 
				print("Missing: {0}".format(tf))
				tile = None

	extT, extL = num2deg(xmin,ymin,zoom)
	extB, extR = num2deg(xmax+1,ymax+1,zoom)

	fig, ax = plt.subplots(figsize=(xmax-xmin+1, ymax-ymin+1), dpi=256)
	fig.patch.set_facecolor('white')
	ax.axis('off')
	fig.tight_layout()
	ax.set_aspect((ymax-ymin+1) / (xmax-xmin+1))
	plt.imshow(np.asarray(a), extent=[extL, extR, extB, extT])

	return a


parser = argparse.ArgumentParser(description='Create an image of a track overlayed on a map')

parser.add_argument('file', help='CSV file to use')
parser.add_argument('-o', '--output', help='Output PNG image.')
parser.add_argument('-z', '--zoom', type=int, default=11, help='Zoom level (default 11)')

args = parser.parse_args()


df = pd.read_csv(args.file, index_col='time', parse_dates=True)

drawImageCluster(min(df['lat']), min(df['lon']), max(df['lat']), max(df['lon']), args.zoom)
plt.plot(df['lon'], df['lat'])

if not args.output:
	plt.show()
else:
	plt.savefig(args.output)





