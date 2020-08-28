import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import argparse

parser = argparse.ArgumentParser(description='Create a graph')

parser.add_argument('file', help='CSV file to use')
parser.add_argument('column', help='Column to plot')
parser.add_argument('-o', '--output', help='Output PNG image.')
parser.add_argument('-s', '--smooth', type=int, default=20, help='Output PNG image.')

args = parser.parse_args()

df = pd.read_csv(args.file, index_col='time', parse_dates=True)

d = df[args.column]
df[args.column + "'"] = np.convolve( \
    np.concatenate((np.ones(args.smooth)*d.iat[0], d, np.ones(args.smooth)*d.iat[-1])), \
    np.ones(args.smooth * 2 + 1) / (args.smooth * 2 + 1), \
    mode="valid")

df.plot('elapsed', args.column + "'")

if not args.output:
    plt.show()
else:
    plt.savefig(args.output)





