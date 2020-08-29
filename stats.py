import pandas as pd
import numpy as np
import time
import datetime

import argparse

parser = argparse.ArgumentParser(description='Show summary stats')

parser.add_argument('file', help='CSV file to use')

args = parser.parse_args()
df = pd.read_csv(args.file, index_col='time', parse_dates=True)


print("Distance: {0:.2f}km".format(df['s'].iat[-1]))

print("Moving Time: {0}".format(str(datetime.timedelta(seconds=df['elapsed'].iat[-1]))))

time_series = df.index.to_series()
print("Total Time: {0}".format(time_series.iat[-1] - time_series.iat[0]))


v = df['vel'].loc[np.equal(df['moving'], 1)]
print("Average Speed: {0:.2f}km/h".format( df['s'].iat[-1] * 3600 / df['elapsed'].iat[-1] ))

print("Max Speed: {0:.2f}km/h".format(v.max()))

print("Ascent: {0:.0f}m".format(df['asc'].iat[-1]))
print("Descent: {0:.0f}m".format(df['desc'].iat[-1]))

