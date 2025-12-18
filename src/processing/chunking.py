import json, os

def split_json(input_file, output_dir, chunk_size=1000):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        out = f"{output_dir}/chunk_{i//chunk_size}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(chunk, f, indent=2)
