import pandas as pd

def find_missing(valid_csv, processed_csv, output_csv):
    valid = set(pd.read_csv(valid_csv)["appid"])
    processed = set(pd.read_csv(processed_csv)["appid"])

    missing = valid - processed
    if missing:
        pd.DataFrame({"appid": list(missing)}).to_csv(output_csv, index=False)
    return len(missing)