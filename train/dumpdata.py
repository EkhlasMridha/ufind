import pandas as pd
import numpy as np
import os.path

f_name = "face_data.csv"


def write(foundId, data):
    if os.path.isfile(f_name):
        df = pd.read_csv(f_name, index_col=0)
        latest = pd.DataFrame(data, columns=map(str, range(10000)))

        latest['id'] = foundId

        df = pd.concat((df, latest), ignore_index=True, sort=False)

    else:
        df = pd.DataFrame(data, columns=map(str, range(10000)))
        df['id'] = foundId

    df.to_csv(f_name)
