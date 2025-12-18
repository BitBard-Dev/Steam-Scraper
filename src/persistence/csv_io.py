import os
import pandas as pd

def append_rows(csv_path, rows, headers):
    df = pd.DataFrame(rows, columns=headers)
    if not os.path.exists(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode="a", index=False, header=False)