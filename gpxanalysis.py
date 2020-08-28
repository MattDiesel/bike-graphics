
import pandas as pd
import numpy as np
import datetime


def gpxAnalyse(df):
    lonr1, latr1 = map(np.radians, [df['lon'], df['lat']])
    lonr2 = np.roll(lonr1,1)
    lonr2[0] = lonr2[1]
    latr2 = np.roll(latr1,1)
    latr2[0] = latr2[1]

    dz = df['alt'].diff()
    dt = df.index.to_series().diff() / datetime.timedelta(seconds=1)

    a = np.sin((latr2-latr1)*0.5)**2 + np.cos(latr1)*np.cos(latr2)*np.sin((lonr2-lonr1)*0.5)**2
    ds = np.sqrt((6372800 * 2 * np.arcsin(np.sqrt(a)))**2 + dz**2)

    df['vel'] = (ds / dt) * 3.6
    df['moving'] = np.logical_and(np.greater(df['vel'], 0.2), np.less(dt, 30)).astype(int)
    df['s'] = np.cumsum(ds * df['moving']) / 1000
    df['elapsed'] = np.cumsum(dt * df['moving'])
    df['asc'] = np.cumsum(dz * (dz > 0) * df['moving'])
    df['desc'] = np.cumsum(dz * (dz < 0) * df['moving'])

    return df

